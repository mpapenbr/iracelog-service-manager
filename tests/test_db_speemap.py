from sqlalchemy.orm import Session

from iracelog_service_manager.db.schema import Event
from iracelog_service_manager.db.schema import Speedmap
from iracelog_service_manager.persistence.access import read_event_speedmap_latest_entry
from iracelog_service_manager.persistence.access import read_event_speedmap_latest_entry_by_key
from iracelog_service_manager.persistence.service import session_read_speedmap_data
from iracelog_service_manager.persistence.access import read_events
from iracelog_service_manager.persistence.util import orm_session


def test_read_latest_entry(testOrm: Session):
    e1 = Event(name="event1", eventKey="key1")
    testOrm.add(e1)
    e2 = Event(name="event2", eventKey="key2")
    testOrm.add(e2)
    testOrm.flush()
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176130}))
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176140}))
    testOrm.add(Speedmap(eventId=e2.id, data={'timestamp': 1700000000}))  # just dummy data for another event

    res = read_event_speedmap_latest_entry(testOrm, e1.id)
    assert res is not None
    assert res.data['timestamp'] == 1665176140

    res = read_event_speedmap_latest_entry_by_key(testOrm, e1.eventKey)
    assert res is not None
    assert res.data['timestamp'] == 1665176140


def test_read_archived(testOrm: Session):
    e1 = Event(name="event1", eventKey="key1")
    testOrm.add(e1)
    e2 = Event(name="event2", eventKey="key2")
    testOrm.add(e2)
    testOrm.flush()
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176130}))
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176140}))
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176150}))
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176160}))
    testOrm.add(Speedmap(eventId=e2.id, data={'timestamp': 1700000000}))  # just dummy data for another event

    # we need the data to be persisted now (otherwise data seems to be not available for next call)
    testOrm.commit()

    # execute
    unwrapped = session_read_speedmap_data.__wrapped__
    con = testOrm.get_bind()
    res = unwrapped(con, e1.id, 1665176130, 2)  # the query is gt (>)

    assert res is not None
    assert len(res) == 2
    assert res[0]['timestamp'] == 1665176140
    assert res[1]['timestamp'] == 1665176150
