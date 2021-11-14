from sqlalchemy.engine.base import Connection
from sqlalchemy.orm.session import Session

from iracelog_service_manager.db.schema import Event

from .util import orm_session


def read_events(s:Session):
    res = s.query(Event).all()
    return res


def read_event_info(s:Session, eventId:int):
    res = s.query(Event).filter_by(Id=eventId).first()
    return res