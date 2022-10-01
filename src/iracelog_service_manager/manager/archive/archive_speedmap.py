from dataclasses import dataclass

from autobahn.asyncio.wamp import ApplicationSession

from iracelog_service_manager.model.message import Message
from iracelog_service_manager.persistence.service import session_store_speedmap_msg


@dataclass
class ArchiveSpeedmap:
    """handles the archiving of incoming speedmap messages for an event"""
    s : ApplicationSession
    """holds the WAMP session"""
    eventId: int
    """the event id to record"""
    topic: str
    """the topic for the speedmap messages from racelogger"""

    async def start_recording(self):
        self.s.log.info(f"listening to {self.topic}")
        self._subscription = await self.s.subscribe(self.record, self.topic)
        print(f"got subscription {self._subscription}")
        pass
    def stop_recording(self):
        self._subscription.unsubscribe()
        pass

    def record(self, msg: Message):        
        session_store_speedmap_msg(self.eventId, msg)
        

