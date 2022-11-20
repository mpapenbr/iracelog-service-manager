from sqlalchemy.orm import Session

from iracelog_service_manager.db.schema import Event
from iracelog_service_manager.db.schema import Speedmap
from iracelog_service_manager.persistence.access import read_event_speedmap_latest_entry
from iracelog_service_manager.persistence.access import read_event_speedmap_latest_entry_by_key
from iracelog_service_manager.persistence.service import session_avglap_over_time_date_bin, session_read_speedmap_data
from iracelog_service_manager.persistence.access import read_events
from iracelog_service_manager.persistence.util import orm_session


def test_compose_avg_laptimes_over_time(testOrm: Session):
    e1 = Event(name="event1", eventKey="key1", data={"info": {"speedmapInterval": 10}})
    testOrm.add(e1)
    e2 = Event(name="event2", eventKey="key2")
    testOrm.add(e2)
    testOrm.flush()
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176130, "payload": {
                "data": {"c1": {"laptime": 10, "chunkSpeeds": [100, 120, 0]}}, "sessionTime": 10, "timeOfDay": 20, "trackTemp": 25.2, "chunkSize": 10, "trackLength": 30}}))
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176140, "payload": {
                "data": {"c1": {"laptime": 10, "chunkSpeeds": [200, 120, 130]}}, "sessionTime": 10, "timeOfDay": 20, "trackTemp": 25.2, "chunkSize": 10, "trackLength": 30}}))
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176150, "payload": {
                "data": {"c1": {"laptime": 10, "chunkSpeeds": [105, 115, 130]}}, "sessionTime": 10, "timeOfDay": 20, "trackTemp": 25.2, "chunkSize": 10, "trackLength": 30}}))
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176160, "payload": {
                "data": {"c1": {"laptime": 10, "chunkSpeeds": [95, 115, 130]}}, "sessionTime": 10, "timeOfDay": 20, "trackTemp": 25.2, "chunkSize": 10, "trackLength": 30}}))
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176170, "payload": {
                "data": {"c1": {"laptime": 10, "chunkSpeeds": [95, 115, 130]}}, "sessionTime": 10, "timeOfDay": 20, "trackTemp": 25.2, "chunkSize": 10, "trackLength": 30}}))

    testOrm.add(Speedmap(eventId=e2.id, data={'timestamp': 1700000000}))  # just dummy data for another event

    # we need the data to be persisted now (otherwise data seems to be not available for next call)
    testOrm.commit()

    # execute
    unwrapped = session_avglap_over_time_date_bin.__wrapped__
    con = testOrm.get_bind()
    res = unwrapped(con, e1.id, 20)

    assert res is not None
    assert len(res) == 2
