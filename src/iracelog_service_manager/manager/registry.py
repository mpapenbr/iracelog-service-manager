from dataclasses import dataclass
import dataclasses

from autobahn.asyncio.wamp import ApplicationSession, Session
from iracelog_service_manager.model.eventlookup import EventLookup, ProviderData

@dataclass
class Registry:
    """handles registration of race data providers"""
    appSession : ApplicationSession
    """holds the WAMP session"""
    events: EventLookup
    """lookup for provider"""


    def __post_init__(self):
        self.appSession.register(self.register_provider, 'racelog.dataprovider.register_provider')
        self.appSession.register(self.remove_provider, 'racelog.dataprovider.remove_provider')
        self.appSession.register(self.list_providers, 'racelog.public.list_providers')

    def register_provider(self, data:any):
        print(f"{data}")        
        x = ProviderData(eventKey=data['eventKey'],manifests=data['manifests'], info=data['info'])
        print(x)
        if data['eventKey'] in self.events.lookup:
            raise Exception("already there")
        self.events.lookup[data['eventKey']] = x
        # TODO: create db entry
        # TODO: announce new provider
    
    def remove_provider(self, eventKey:str):
        if eventKey in self.events.lookup:
            self.events.lookup.pop(eventKey)
            # TODO: announce removed provider
            return "provider removed"
        else:
            return f"No provider for {eventKey} "
    
    

    
    def list_providers(self) -> list[ProviderData]:
        
        ret = [dataclasses.asdict(v) for v in self.events.lookup.values()]
        print(ret)
        return ret
