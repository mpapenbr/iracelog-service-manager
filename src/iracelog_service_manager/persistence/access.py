from sqlalchemy.engine.base import Connection
from sqlalchemy.orm.session import Session

from iracelog_service_manager.db.schema import AnalysisData
from iracelog_service_manager.db.schema import Event
from iracelog_service_manager.db.schema import TrackData


def read_events(s:Session):
    """read all events (ordered by recordDate - latest first)"""
    res = s.query(Event).order_by(Event.recordDate.desc()).all()
    return res


def read_event_info(s:Session, eventId:int) -> Event:
    """read a single event by its eventId"""
    res = s.query(Event).filter_by(id=eventId).first()
    return res

def read_event_info_by_key(s:Session, eventKey:str) -> Event:
    """read a single event by its eventKey"""
    res = s.query(Event).filter_by(eventKey=eventKey).first()
    return res

def read_event_analysis(s:Session, eventId:int) -> AnalysisData:
    """read the analysis data  by its eventId"""
    res = s.query(AnalysisData).filter_by(eventId=eventId).first()    
    return res


def read_track_info(s:Session, trackId:int) -> TrackData:
    """read track data by trackId"""
    res = s.query(TrackData).filter_by(id=trackId).first()
    return res



def store_event(s:Session, e:Event):
    """store an event"""
    s.add(e)
    
