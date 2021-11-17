from dataclasses import dataclass
from os import name

from autobahn.asyncio.wamp import ApplicationSession
from autobahn.asyncio.wamp import Session

from iracelog_service_manager.db.schema import Event
from iracelog_service_manager.manager.commands import CommandType
from iracelog_service_manager.manager.commands import ManagerCommand
from iracelog_service_manager.model.eventlookup import ProviderData
from iracelog_service_manager.persistence.access import store_event
from iracelog_service_manager.persistence.service import session_store_event
from iracelog_service_manager.persistence.util import DbHandler
from iracelog_service_manager.persistence.util import orm_session
from iracelog_service_manager.persistence.util import tx


@dataclass
class Archiver:
    """holds the WAMP session"""
    s : ApplicationSession

    def __post_init__(self):
        self._commandSwitch = {
            CommandType.REGISTER: self.cmd_register,
            CommandType.UNREGISTER: self.cmd_unregister
        }
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
        session_store_event(payload)
        # with DbHandler().new_session() as session:
        #     with session.begin():            
        #         store_event(session, Event(
        #             eventKey=payload.eventKey,
        #             name=payload.info.name,
        #             description=payload.info.description if 'description' in payload.info else "",
        #             data=payload.info))
        self.s.subscribe(self.providerAnnouncement, f'racelog.dataprovider.state.{payload.eventKey}')
        pass
    def cmd_unregister(self, payload: str):
        print(f"received unregister payload: {payload}")
        pass

    
    