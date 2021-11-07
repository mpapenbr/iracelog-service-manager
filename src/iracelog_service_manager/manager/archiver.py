from dataclasses import dataclass

from autobahn.asyncio.wamp import ApplicationSession, Session

@dataclass
class Archiver:
    """holds the WAMP session"""
    s : ApplicationSession

    def __post_init__(self):
        self.s.subscribe(self.something, 'racelog.dataprovider.dummy')

    def something(self, data:any):
        print(f"{data}")