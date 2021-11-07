"""
this module handles manages race data provider
"""
from autobahn.asyncio.wamp import ApplicationSession

from iracelog_service_manager.manager.archiver import Archiver
from iracelog_service_manager.manager.registry import Registry

import asyncio

from iracelog_service_manager.model.eventlookup import EventLookup

class ProviderManager(ApplicationSession):
    """
    handles register and removal of race data provider
    we expect the following structure in config.exta

    {
        realm: <crossbar-realm>
        user: <username>
        password: <password>
        events: EventLookup
    }
    """

    def onConnect(self):
        self.log.info("Client connected: {klass}", klass=ProviderManager)
        self.join(self.config.realm, authid=self.config.extra['user'], authmethods=["ticket"])

    def onChallenge(self, challenge):
        self.log.info("Challenge for method {authmethod} received", authmethod=challenge.method)
        return self.config.extra['password']
    
    def onLeave(self, details):
        self.log.info("Router session closed ({details})", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("Router connection closed")

    async def onJoin(self, details):
        self.log.info("joined {details}", details=details)
        try:
            events = EventLookup()
            archiver = Archiver(self)
            registry = Registry(appSession=self, events=events)

            
        except Exception as e:
            self.log.error("Got exception {e}", e=e)
            self.leave()
        
    def onDisconnect(self):
        asyncio.get_event_loop().stop()
