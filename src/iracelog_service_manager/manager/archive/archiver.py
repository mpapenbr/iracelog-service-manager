import asyncio

from dataclasses import dataclass
from os import name

from autobahn.asyncio.wamp import ApplicationSession
from autobahn.asyncio.wamp import Session

from iracelog_service_manager.db.schema import Event
from iracelog_service_manager.manager.archive.archive_event import ArchiveEvent
from iracelog_service_manager.manager.commands import CommandType
from iracelog_service_manager.manager.commands import ManagerCommand
from iracelog_service_manager.model.eventlookup import ProviderData
from iracelog_service_manager.persistence.access import store_event
from iracelog_service_manager.persistence.service import session_process_new_event, session_store_state_msg
from iracelog_service_manager.persistence.util import DbHandler
from iracelog_service_manager.persistence.util import orm_session
from iracelog_service_manager.persistence.util import tx_session


@dataclass
class Archiver:
    """handles the archiving of incoming state messages for an event"""
    s : ApplicationSession
    """holds the WAMP session"""

    def __post_init__(self):
        self._commandSwitch = {
            CommandType.REGISTER: self.cmd_register,
            CommandType.UNREGISTER: self.cmd_unregister
        }
        self._archiver_lookup = {}
        self.s.subscribe(self.providerAnnouncement, 'racelog.manager.provider')

    def providerAnnouncement(self, wampData:ManagerCommand):
        # print(f"{wampData}")
        data = ManagerCommand(**wampData)

        if (data.type in self._commandSwitch):
            # print(f"I know you {data.type}")
            self._commandSwitch[data.type](data.payload)
        else:
            print(f"What are you {data.type}")

    def eventCommandHandler(self, data:any):
        print(f"command recieved {data}")

    
    
    def cmd_register(self,wampPayload: ProviderData):
        print(f"received register payload: {wampPayload}")
        payload = ProviderData(**wampPayload)
        
        event_recorder = ArchiveEvent(self.s, payload.dbId, f'racelog.public.live.state.{payload.eventKey}')
        self._archiver_lookup[payload.eventKey] = event_recorder
        asyncio.create_task(event_recorder.start_recording())
        pass

    def cmd_unregister(self, payload: str):
        print(f"received unregister payload: {payload}")
        if payload in self._archiver_lookup.keys():
            self._archiver_lookup[payload].stop_recording()
        pass

    

    
    