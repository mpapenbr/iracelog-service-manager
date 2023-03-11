from dataclasses import dataclass

from autobahn.asyncio.wamp import ApplicationSession
from sqlalchemy.orm import Session

from iracelog_service_manager.persistence.access import read_event_info
from iracelog_service_manager.persistence.maintenance import dev_fix_speedmaps
from iracelog_service_manager.persistence.service import session_remove_event
from iracelog_service_manager.persistence.util import db_session


@dataclass
class AdminAccess:
    """handles endpoints for admin access to archived data"""
    s: ApplicationSession
    """holds the WAMP session"""

    def __post_init__(self):
        self.s.register(self.delete_event, 'racelog.admin.event.delete')
        #
        # self.s.register(self.speedmap_fix, 'racelog.admin.event.speedmapfix')

    def delete_event(self, eventId):
        """removes an event with all data from the database"""
        self.s.log.info("deleting event {eventId}", eventId=eventId)
        session_remove_event(eventId)

    def speedmap_fix(self, eventId):
        """tmp: fixes speedmap entries (currently not in use)"""
        self.s.log.info("fixing speedmap for  {eventId}", eventId=eventId)

        dev_fix_speedmaps(eventId)
