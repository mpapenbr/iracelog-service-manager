import json

from sqlalchemy import text
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from iracelog_service_manager.db.schema import AnalysisData
from iracelog_service_manager.db.schema import Driver
from iracelog_service_manager.db.schema import Event
from iracelog_service_manager.db.schema import EventExtraData
from iracelog_service_manager.db.schema import Speedmap
from iracelog_service_manager.db.schema import TrackData
from iracelog_service_manager.db.schema import WampData
from iracelog_service_manager.model.eventlookup import ProviderData
from iracelog_service_manager.model.message import Message
from iracelog_service_manager.model.message import MessageType
from iracelog_service_manager.persistence.access import read_events
from iracelog_service_manager.persistence.access import read_track_info
from iracelog_service_manager.persistence.access import store_event
from iracelog_service_manager.persistence.util import db_connection
from iracelog_service_manager.persistence.util import db_session
from iracelog_service_manager.persistence.util import tx_connection
from iracelog_service_manager.persistence.util import tx_session


@tx_session
def session_process_new_event(s: Session, payload: ProviderData):
    """
    extracts data from ProviderData and creates a new entry in the database.
    the id of the created event is stored in payload.dbId
    also: an track entry is created if none exits.
    """
    # print(payload)
    e = Event(
        eventKey=payload.eventKey,
        name=payload.info['name'],
        description=payload.info['description'] if 'description' in payload.info else "",
        data={'info': payload.info, 'manifests': payload.manifests})
    store_event(s, e)
    s.flush()
    payload.dbId = e.id
    # print(f"session_store_event: {e.__dict__}")
    t = read_track_info(s, payload.info['trackId'])
    if (t == None):
        t = TrackData(id=payload.info['trackId'],
                      data={
            'trackId': payload.info['trackId'],
            'sectors': payload.info['sectors'],
            'trackLength': payload.info['trackLength'],
            'trackDisplayName': payload.info['trackDisplayName'],
            'trackDisplayShortName': payload.info['trackDisplayShortName'],
            'trackConfigName': payload.info['trackConfigName']
        })
        s.add(t)


@tx_connection
def session_remove_event(con: Connection, eventId: int):
    """
    removes an event (including data) from the database
    """
    con.execute(text(f"delete from {WampData.__tablename__} where event_id=:eventId").bindparams(eventId=eventId))
    con.execute(text(f"delete from {AnalysisData.__tablename__} where event_id=:eventId").bindparams(eventId=eventId))
    con.execute(text(f"delete from {EventExtraData.__tablename__} where event_id=:eventId").bindparams(eventId=eventId))
    con.execute(text(f"delete from {Driver.__tablename__} where event_id=:eventId").bindparams(eventId=eventId))
    con.execute(text(f"delete from {Speedmap.__tablename__} where event_id=:eventId").bindparams(eventId=eventId))
    con.execute(text(f"delete from {Event.__tablename__} where id=:eventId").bindparams(eventId=eventId))


@tx_session
def session_store_event_extra_data(s: Session, eventId: int, payload: dict):
    """
    stores extra event data in own table. Additionally checks if TrackData for the used
    track already exists. If not they will be created.
    """
    extra_data = EventExtraData(eventId=eventId, data=payload)
    s.add(extra_data)
    trackId = payload['track']['trackId']
    res = s.query(TrackData).filter_by(id=trackId).first()
    if res is None:
        s.add(TrackData(id=trackId, data=payload['track']))
    else:
        if 'pit' not in res.data:
            res.data['pit'] = payload['track']['pit']
            # tell orm session that attr 'data' is modified
            # otherwise it won't get persisted
            flag_modified(res, 'data')

            # the other way would be the following
            # Don't know which is one is more ugly

            # new_data = dict(res.data)
            # new_data['pit'] = payload['track']['pit']
            # res.data = new_data

        pass


@tx_session
def session_store_state_msg(s: Session, eventId: int, payload: dict):
    w = WampData(eventId=eventId, data=payload)
    s.add(w)


@tx_session
def session_store_speedmap_msg(s: Session, eventId: int, payload: dict):
    sm = Speedmap(eventId=eventId, data=payload)
    s.add(sm)


@tx_session
def session_store_driver_msg(s: Session, eventId: int, payload: dict):
    res = s.query(Driver).filter_by(eventId=eventId).first()
    if res is None:
        s.add(Driver(eventId=eventId, data=payload))
    else:
        res.data = payload
        # tell orm session that attr 'data' is modified
        # otherwise it won't get persisted
        flag_modified(res, 'data')


@db_session
def session_read_events(dbSession: Session) -> dict:
    res = dbSession.query(Event).order_by(Event.recordDate.desc()).all()
    return [item.toDict() for item in res]


@db_connection
def session_read_wamp_data_with_diff(con: Connection, eventId=None, tsBegin=None, num=10) -> list[dict]:
    """collect a number of messages from table WAMPDATA.
    the first row of the result is the full data from the database and will be included "as is" (MessageType.STATE)
    the following rows contain just the delta to the previous row.
    we use a special message type for this data (MessageType.STATE_DELTA).
    """
    def compute_car_changes(ref, cur):
        changes = []
        # carsRef = ref[0]['payload']['cars']
        # carsCur = cur[0]['payload']['cars']
        for i in range(len(cur)):
            for j in range(len(cur[i])):
                if i < len(ref) and j < len(ref[i]):
                    if ref[i][j] != cur[i][j]:
                        changes.append([i, j, cur[i][j]])
                else:
                    changes.append([i, j, cur[i][j]])
        return changes

    def compute_session_changes(ref, cur):
        changes = []
        for i in range(len(cur)):
            if i < len(ref):
                if ref[i] != cur[i]:
                    changes.append([i, cur[i]])
            else:
                changes.append([i, cur[i]])
        return changes

    res = con.execute(text("""
    select data from wampdata 
    where event_id=:eventId and (data->'timestamp')::numeric > :tsBegin 
    order by (data->'timestamp')::numeric asc 
    limit :num
    """).bindparams(eventId=eventId, tsBegin=tsBegin, num=num))

    if res.rowcount == 0:
        return []
    work = [row[0] for row in res]
    ret = [work[0]]
    ref = work[0]
    for cur in work[1:]:
        entry = {
            'cars': compute_car_changes(ref['payload']['cars'], cur['payload']['cars']),
            'session': compute_session_changes(ref['payload']['session'], cur['payload']['session']),
        }
        ret.append({'type': MessageType.STATE_DELTA.value, 'payload': entry, 'timestamp': cur['timestamp']})
        ref = cur

    return ret
