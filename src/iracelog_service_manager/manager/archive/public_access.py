from dataclasses import dataclass

from autobahn.asyncio.wamp import ApplicationSession
from sqlalchemy.orm import Session

from iracelog_service_manager.db.schema import Event
from iracelog_service_manager.persistence.access import read_event_analysis, read_event_speedmap_latest_entry, read_event_speedmap_latest_entry_by_key
from iracelog_service_manager.persistence.access import read_event_cars
from iracelog_service_manager.persistence.access import read_event_cars_by_key
from iracelog_service_manager.persistence.access import read_event_info
from iracelog_service_manager.persistence.access import read_event_info_by_key
from iracelog_service_manager.persistence.access import read_events
from iracelog_service_manager.persistence.access import read_track_info
from iracelog_service_manager.persistence.service import session_read_events
from iracelog_service_manager.persistence.service import session_read_wamp_data_with_diff
from iracelog_service_manager.persistence.util import DbHandler
from iracelog_service_manager.persistence.util import db_session
from iracelog_service_manager.persistence.util import orm_session
from iracelog_service_manager.persistence.util import tx_session


@dataclass
class PublicAccess:
    """handles endpoints for public access to archived data"""

    s: ApplicationSession
    """holds the WAMP session"""

    def __post_init__(self):
        self.s.register(self.get_events, 'racelog.public.get_events')
        self.s.register(self.get_event_info, 'racelog.public.get_event_info')
        self.s.register(self.get_event_info_by_key, 'racelog.public.get_event_info_by_key')
        self.s.register(self.get_track_info, 'racelog.public.get_track_info')
        self.s.register(self.get_event_cars, 'racelog.public.get_event_cars')
        self.s.register(self.get_event_cars_by_key, 'racelog.public.get_event_cars_by_key')
        self.s.register(self.get_event_speedmap, 'racelog.public.get_event_speedmap')
        self.s.register(self.get_event_speedmap_by_key, 'racelog.public.get_event_speedmap_by_key')
        self.s.register(self.get_event_analysis, 'racelog.public.archive.get_event_analysis')
        self.s.register(self.get_archived_states_delta, 'racelog.public.archive.state.delta')

    def get_events(self) -> dict:
        """reads all events ordered by recorded data desc (latest first)"""
        @db_session
        def internal_read(dbSession: Session):
            res = read_events(dbSession)
            return [item.toDict() for item in res]
        return internal_read()

    def get_event_info(self, eventId: int) -> dict:
        """reads event data by eventId"""
        @db_session
        def internal_read(dbSession: Session):
            res = read_event_info(dbSession, eventId)
            if res is not None:
                return res.toDict()
            return None
        return internal_read()

    def get_event_info_by_key(self, eventKey: str) -> dict:
        """reads event data by eventKey"""
        @db_session
        def internal_read(dbSession: Session):
            res = read_event_info_by_key(dbSession, eventKey)
            if res is not None:
                return res.toDict()
            return None
        return internal_read()

    def get_event_analysis(self, eventId) -> dict:
        """reads event analysis data by eventId"""
        @db_session
        def internal_read(dbSession: Session):
            res = read_event_analysis(dbSession, eventId)
            if res is not None:
                return res.data
            return None
        return internal_read()

    def get_track_info(self, trackId) -> dict:
        """reads track data by trackId"""
        @db_session
        def internal_read(dbSession: Session):
            res = read_track_info(dbSession, trackId)
            if res is not None:
                return res.data
            return None
        return internal_read()

    def get_event_cars(self, eventId: int) -> dict:
        """reads driver data (including car infos) by eventId"""
        @db_session
        def internal_read(dbSession: Session):
            res = read_event_cars(dbSession, eventId)
            if res is not None:
                return res.data
            return None
        return internal_read()

    def get_event_cars_by_key(self, eventKey: str) -> dict:
        """reads driver data (including car infos) by eventKey"""
        @db_session
        def internal_read(dbSession: Session):
            res = read_event_cars_by_key(dbSession, eventKey)
            if res is not None:
                return res.data
            return None
        return internal_read()

    def get_event_speedmap(self, eventId: int) -> dict:
        """reads the latest speedmap data by eventId"""
        @db_session
        def internal_read(dbSession: Session):
            res = read_event_speedmap_latest_entry(dbSession, eventId)
            if res is not None:
                return res.data
            return None
        return internal_read()

    def get_event_speedmap_by_key(self, eventKey: str) -> dict:
        """reads the latest speedmap data by eventKey"""
        @db_session
        def internal_read(dbSession: Session):
            res = read_event_speedmap_latest_entry_by_key(dbSession, eventKey)
            if res is not None:
                return res.data
            return None
        return internal_read()

    def get_archived_states_delta(self, eventId: int, ts_begin: int, num: int) -> list[dict]:
        """reads a range of states for an event"""
        return session_read_wamp_data_with_diff(eventId=eventId, tsBegin=ts_begin, num=num)
