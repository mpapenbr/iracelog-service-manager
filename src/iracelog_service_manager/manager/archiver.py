from dataclasses import dataclass

from autobahn.asyncio.wamp import ApplicationSession
from autobahn.asyncio.wamp import Session


@dataclass
class Archiver:
    """holds the WAMP session"""
    s : ApplicationSession

    def __post_init__(self):
        self.s.subscribe(self.providerAnnouncement, 'racelog.manager.provider')

    def providerAnnouncement(self, data:any):
        print(f"{data}")
        # self.s.subscribe(self.evenCommandHandler, f"racelog.manager.command.{data['eventKey']}")

    def eventCommandHandler(self, data:any):
        print(f"command recieved {data}")