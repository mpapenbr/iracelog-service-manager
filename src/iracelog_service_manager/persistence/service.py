from sqlalchemy.orm import Session

from iracelog_service_manager.db.schema import Event
from iracelog_service_manager.model.eventlookup import ProviderData
from iracelog_service_manager.persistence.access import store_event
from iracelog_service_manager.persistence.util import tx


@tx
def session_store_event(s:Session, payload:ProviderData):    
    """extracts data from ProviderData and creates a new entry in the database"""
    # print(payload)
    store_event(s, Event(
        eventKey=payload.eventKey,
        name=payload.info['name'],
        description=payload.info['description'] if 'description' in payload.info else "",
        data=payload.info))