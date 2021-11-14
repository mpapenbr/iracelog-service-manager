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

    Id = Column(Integer, name="id", primary_key=True, autoincrement=True, nullable=False)
    EventKey = Column(String, name="event_key", unique=True)
    Name = Column(String, name="name")
    Description = Column(String,name="description", nullable=True)
    RecordDate = Column(TIMESTAMP, name="record_stamp", nullable=False, server_default=text('now()'))
    Data = Column(postgresql.JSONB, name="data")

    def toDict(self) -> str:
        return {"id":self.Id, "eventKey": self.EventKey, "name": self.Name, "description": self.Description, "data": self.Data, "recordDate": self.RecordDate.isoformat()}

class WampData(Base):
    __tablename__ = "wampdata"
    Id = Column(Integer, name="id", primary_key=True)        
    EventId = Column(Integer, ForeignKey("event.id"),  name="event_id", nullable=False)
    Data = Column(postgresql.JSONB, name="data")    
    Event = relationship("Event")

class AnalysisData(Base):
    __tablename__ = "analysis"
    Id = Column(Integer, name="id", primary_key=True)        
    EventId = Column(Integer, ForeignKey("event.id"),  name="event_id", nullable=False)
    Data = Column(postgresql.JSONB, name="data")        

class TrackData(Base):
    __tablename__ = "track"
    Id = Column(Integer, name="id", primary_key=True)            
    Data = Column(postgresql.JSONB, name="data")        


class EventExtraData(Base):
    """
    contains data collected during event which may be usesful some time ;)
    """
    __tablename__ = "event_ext"
    Id = Column(Integer, name="id", primary_key=True)            
    EventId = Column(Integer, ForeignKey("event.id"),  name="event_id", nullable=False)
    Data = Column(postgresql.JSONB, name="data")        

