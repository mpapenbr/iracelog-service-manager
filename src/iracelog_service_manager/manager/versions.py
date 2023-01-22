

from dataclasses import dataclass

from autobahn.asyncio.wamp import ApplicationSession

from iracelog_service_manager import __version__ as my_version


@dataclass
class Versions:
    """handles version requests"""
    appSession: ApplicationSession
    """holds the WAMP session"""

    def __post_init__(self):
        self.appSession.register(self.get_versions, 'racelog.public.get_version')

    def get_versions(self) -> dict:
        """returns current version informations"""

        ret = {'ownVersion': my_version}
        return ret
