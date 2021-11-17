from sqlalchemy.engine.base import Connection
from sqlalchemy.orm.session import Session

from iracelog_service_manager.db.schema import Event
from iracelog_service_manager.db.schema import TrackData


def read_events(s:Session):
    """read all events"""
    res = s.query(Event).all()
    return res


def read_event_info(s:Session, eventId:int):
    """read a single event by its eventId"""
    res = s.query(Event).filter_by(Id=eventId).first()
    return res

def read_event_info_by_key(s:Session, eventKey:str):
    """read a single event by its eventKey"""
    res = s.query(Event).filter_by(EventKey=eventKey).first()
    return res

def read_track_info(s:Session, trackId:int):
    """read track data by trackId"""
    res = s.query(TrackData).filter_by(Id=trackId).first()
    return res


def store_event(s:Session, e:Event):
    """store an event"""
    s.add(e)
    
