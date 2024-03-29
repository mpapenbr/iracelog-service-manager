
import dataclasses
from dataclasses import dataclass
from datetime import datetime

from autobahn.asyncio.wamp import ApplicationSession
from autobahn.asyncio.wamp import Session

from iracelog_service_manager.manager.commands import CommandType
from iracelog_service_manager.manager.commands import ManagerCommand
from iracelog_service_manager.model.eventlookup import EventLookup
from iracelog_service_manager.model.eventlookup import ProviderData
from iracelog_service_manager.persistence.service import session_process_new_event
from iracelog_service_manager.persistence.service import session_store_event_extra_data


@dataclass
class Registry:
    """handles registration of race data providers"""
    appSession: ApplicationSession
    """holds the WAMP session"""
    events: EventLookup
    """lookup for provider"""

    def __post_init__(self):
        self.appSession.register(self.register_provider, 'racelog.dataprovider.register_provider')
        self.appSession.register(self.remove_provider, 'racelog.dataprovider.remove_provider')
        self.appSession.register(self.process_event_extra_data, 'racelog.dataprovider.store_event_extra_data')
        self.appSession.register(self.list_providers, 'racelog.public.list_providers')

    def register_provider(self, data: any):
        """
        handles registration of a provider
        """
        # print(f"{data}")

        recordDate: float = None

        if 'recordDate' in data:
            recordDate = data['recordDate']

        x = ProviderData(eventKey=data['eventKey'], manifests=data['manifests'],
                         info=data['info'],
                         recordDate=recordDate)
        # print(x)
        if data['eventKey'] in self.events.lookup:
            raise Exception("already there")
        self.events.lookup[data['eventKey']] = x
        # store
        session_process_new_event(x)
        # print(x.__dict__)
        # self.appSession.publish("racelog.manager.provider", {'eventType': 'new', 'eventData': dataclasses.asdict(x)})
        tosend = ManagerCommand(type=CommandType.REGISTER, payload=x.__dict__).__dict__

        # print(tosend)
        self.appSession.publish("racelog.manager.provider", tosend)

    def remove_provider(self, eventKey: str):
        """
        handles the removal of a provider
        """
        if eventKey in self.events.lookup:
            self.events.lookup.pop(eventKey)
            # TODO: announce removed provider
            tosend = ManagerCommand(type=CommandType.UNREGISTER, payload=eventKey).__dict__
            self.appSession.publish("racelog.manager.provider", tosend)
            return "provider removed"
        else:
            return f"No provider for {eventKey} "

    def process_event_extra_data(self, eventKey: str, extraData: dict = {}):
        """
        the provider may send extra data. this is handled here
        """
        if eventKey in self.events.lookup:
            event = self.events.lookup[eventKey]
            session_store_event_extra_data(event.dbId, extraData)

        else:
            return f"No provider for {eventKey} "

    def list_providers(self) -> list[ProviderData]:

        ret = [dataclasses.asdict(v) for v in self.events.lookup.values()]
        print(ret)
        return ret
