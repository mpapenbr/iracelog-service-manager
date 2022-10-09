from sqlalchemy.engine.base import Connection
from sqlalchemy.orm.session import Session

from iracelog_service_manager.db.schema import AnalysisData
from iracelog_service_manager.db.schema import Driver
from iracelog_service_manager.db.schema import Event
from iracelog_service_manager.db.schema import EventExtraData
from iracelog_service_manager.db.schema import Speedmap
from iracelog_service_manager.db.schema import TrackData
from iracelog_service_manager.db.schema import WampData


def read_events(s: Session):
    """read all events (ordered by recordDate - latest first)"""
    res = s.query(Event).order_by(Event.recordDate.desc()).all()
    return res


def read_event_info(s: Session, eventId: int) -> Event:
    """read a single event by its eventId"""
    res = s.query(Event).filter_by(id=eventId).first()
    return res


def read_event_info_by_key(s: Session, eventKey: str) -> Event:
    """read a single event by its eventKey"""
    res = s.query(Event).filter_by(eventKey=eventKey).first()
    return res


def read_event_extra_info(s: Session, eventId: int) -> EventExtraData:
    """read event extra data by eventId"""
    res = s.query(EventExtraData).filter_by(eventId=eventId).first()
    return res


def read_event_analysis(s: Session, eventId: int) -> AnalysisData:
    """read the analysis data  by its eventId"""
    res = s.query(AnalysisData).filter_by(eventId=eventId).first()
    return res


def read_track_info(s: Session, trackId: int) -> TrackData:
    """read track data by trackId"""
    res = s.query(TrackData).filter_by(id=trackId).first()
    return res


def read_wamp_data(s: Session, eventId: int) -> WampData:
    """read wamp data by eventId (just used for tests)"""
    res = s.query(WampData).filter_by(eventId=eventId).all()
    return res


def read_speedmap_data(s: Session, eventId: int) -> Speedmap:
    """read speedmap data by eventId (just used for tests)"""
    res = s.query(Speedmap).filter_by(eventId=eventId).all()
    return res


def read_event_cars(s: Session, eventId: int) -> Driver:
    """read driver data by eventId"""
    res = s.query(Driver).filter_by(eventId=eventId).first()
    return res


def read_event_cars_by_key(s: Session, eventKey: str) -> Driver:
    """read driver data by eventKey"""
    event = s.query(Driver).join(Event, Driver.eventId == Event.id).where(Event.eventKey == eventKey).first()
    return event


def read_event_speedmap_latest_entry(s: Session, eventId: int) -> Speedmap:
    """read the latest speedmap by eventId"""
    # sind id is a bigserial we can get the latest entry by fetching the highest id for that event
    res = s.query(Speedmap).filter_by(eventId=eventId).order_by(Speedmap.id.desc()).limit(1).first()
    return res


def read_event_speedmap_latest_entry_by_key(s: Session, eventKey: str) -> Speedmap:
    """read the latest speedmap by eventKey"""
    # sind id is a bigserial we can get the latest entry by fetching the highest id for that event
    res = s.query(Speedmap).join(Event, Speedmap.eventId == Event.id).where(
        Event.eventKey == eventKey).order_by(Speedmap.id.desc()).limit(1).first()
    return res


def store_event(s: Session, e: Event):
    """store an event"""
    s.add(e)
