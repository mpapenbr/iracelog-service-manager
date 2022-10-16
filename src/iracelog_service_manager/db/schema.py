import os

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.sqltypes import Float

# eng = create_engine(os.environ.get("SQLALCHEMY_URL"))
Base = declarative_base()


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, name="id", primary_key=True, autoincrement=True, nullable=False)
    eventKey = Column(String, name="event_key", unique=True)
    name = Column(String, name="name")
    description = Column(String, name="description", nullable=True)
    recordDate = Column(TIMESTAMP, name="record_stamp", nullable=False, server_default=text('now()'))
    data = Column(postgresql.JSONB, name="data")

    def toDict(self) -> str:
        return {"id": self.id, "eventKey": self.eventKey, "name": self.name, "description": self.description, "data": self.data, "recordDate": self.recordDate.isoformat()}


class WampData(Base):
    __tablename__ = "wampdata"
    id = Column(Integer, name="id", primary_key=True)
    eventId = Column(Integer, ForeignKey("event.id"),  name="event_id", nullable=False)
    data = Column(postgresql.JSONB, name="data")
    event = relationship("Event")


class AnalysisData(Base):
    __tablename__ = "analysis"
    id = Column(Integer, name="id", primary_key=True)
    eventId = Column(Integer, ForeignKey("event.id"),  name="event_id", nullable=False)
    data = Column(postgresql.JSONB, name="data")


class TrackData(Base):
    __tablename__ = "track"
    id = Column(Integer, name="id", primary_key=True)
    data = Column(postgresql.JSONB, name="data")


class EventExtraData(Base):
    """
    contains data collected during event which may be usesful some time ;)
    """
    __tablename__ = "event_ext"
    id = Column(Integer, name="id", primary_key=True)
    eventId = Column(Integer, ForeignKey("event.id"),  name="event_id", nullable=False)
    data = Column(postgresql.JSONB, name="data")


class Speedmap(Base):
    """
    contains speed map data for an event
    """
    __tablename__ = "speedmap"
    id = Column(Integer, name="id", primary_key=True)
    eventId = Column(Integer, ForeignKey("event.id"),  name="event_id", nullable=False)
    data = Column(postgresql.JSONB, name="data")


class CarData(Base):
    """
    contains additional iracing car,driver and team data for an event
    """
    __tablename__ = "car"
    id = Column(Integer, name="id", primary_key=True)
    eventId = Column(Integer, ForeignKey("event.id"),  name="event_id", nullable=False)
    data = Column(postgresql.JSONB, name="data")
