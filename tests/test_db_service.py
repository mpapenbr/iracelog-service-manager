from sqlalchemy.orm import Session

from iracelog_service_manager.persistence.access import read_event_extra_info, read_events
from iracelog_service_manager.persistence.service import session_store_event_extra_data
from iracelog_service_manager.persistence.util import  orm_session
from iracelog_service_manager.db.schema import Event




def test_session_extra_events_with_track_create(testOrm:Session):

    # TODO: current version doesn't succeed. Need to think about tx handling for tests

    # prepare Event
    e = Event(id=1, name="Hallo")
    testOrm.add(e)
    testOrm.flush()

    session_store_event_extra_data(e.id, {'track':{'trackId': 12, 'trackName': "testTrack"}})    
    extra = read_event_extra_info(testOrm, e.id)
    assert extra is not None



