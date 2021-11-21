from dataclasses import dataclass


from autobahn.asyncio.wamp import ApplicationSession

from iracelog_service_manager.persistence.service import session_remove_event


@dataclass
class AdminAccess:
    """handles endpoints for admin access to archived data"""
    s: ApplicationSession
    """holds the WAMP session"""

    def __post_init__(self):
        self.s.register(self.delete_event, 'racelog.admin.event.delete')

    def delete_event(self, eventId):
        """removes an event with all data from the database"""
        self.s.log.info("deleting event {eventId}", eventId=eventId)
        session_remove_event(eventId)
