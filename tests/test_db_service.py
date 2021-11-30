from sqlalchemy.orm import Session

from iracelog_service_manager.persistence.access import read_event_extra_info, read_track_info
from iracelog_service_manager.persistence.service import session_store_event_extra_data
from iracelog_service_manager.db.schema import Event, TrackData


std_extra_data = {'track':{'trackId': 12, 'trackName': "testTrack"}}
full_extra_data = {'track':{'trackId': 12, 'trackName': "testTrack", "pit": {"entry": 34, "exit": 56}}}
full_extra_data_other = {'track':{'trackId': 12, 'trackName': "testTrack", "pit": {"entry": 11, "exit": 22}}}
track_data = {'trackId':12, 'trackName': "testTrack", "pit": {"entry": 34, "exit": 56}}
track_data_partial = {'trackId':12, 'trackName': "testTrack"}

def test_session_extra_events_with_track_create(testOrm:Session):
    # prepare Event
    e = Event(id=1, name="Hallo")
    testOrm.add(e)

    unwrapped = session_store_event_extra_data.__wrapped__
    unwrapped(testOrm, e.id, std_extra_data)    
    extra = read_event_extra_info(testOrm, e.id)
    assert extra is not None    
    assert extra.data == std_extra_data

def test_session_extra_events_do_not_update_pit(testOrm:Session):
    """track has already pit data, do not update track"""
    # prepare Event and track
    e = Event(id=1, name="Hallo")
    testOrm.add(e)
    t = TrackData(id=12, data=track_data)
    testOrm.add(t)

    # execute
    unwrapped = session_store_event_extra_data.__wrapped__    
    unwrapped(testOrm, e.id, full_extra_data_other)    
    
    # check
    track = read_track_info(testOrm, 12)
    assert track.data == track_data

def test_session_extra_events_do_update_pit(testOrm:Session):
    """track exists but has no pit data"""
    # prepare Event and track
    e = Event(id=1, name="Hallo")
    testOrm.add(e)
    t = TrackData(id=12, data=track_data_partial)
    testOrm.add(t)

    # execute
    unwrapped = session_store_event_extra_data.__wrapped__    
    unwrapped(testOrm, e.id, full_extra_data)    
    
    # check
    track = read_track_info(testOrm, 12)
    assert track.data['pit'] == {"entry": 34, "exit": 56}
    assert track.data == track_data
    




