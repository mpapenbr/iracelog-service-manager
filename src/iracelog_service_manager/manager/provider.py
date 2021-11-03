"""
this module handles manages race data provider
"""
from autobahn.asyncio.wamp import ApplicationSession

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
        

