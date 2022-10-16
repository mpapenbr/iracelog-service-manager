from sqlalchemy.orm import Session

from iracelog_service_manager.db.schema import Event
from iracelog_service_manager.db.schema import Speedmap
from iracelog_service_manager.persistence.access import read_event_speedmap_latest_entry
from iracelog_service_manager.persistence.access import read_event_speedmap_latest_entry_by_key
from iracelog_service_manager.persistence.access import read_events
from iracelog_service_manager.persistence.util import orm_session


def test_read_latest_entry(testOrm: Session):
    e1 = Event(name="event1", eventKey="key1")
    testOrm.add(e1)
    e2 = Event(name="event2", eventKey="key2")
    testOrm.add(e2)
    testOrm.flush()
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176130}))
    testOrm.add(Speedmap(eventId=e1.id, data={'timestamp': 1665176140}))
    testOrm.add(Speedmap(eventId=e2.id, data={'timestamp': 1700000000}))  # just dummy data for another event

    res = read_event_speedmap_latest_entry(testOrm, e1.id)
    assert res != None
    assert res.data['timestamp'] == 1665176140

    res = read_event_speedmap_latest_entry_by_key(testOrm, e1.eventKey)
    assert res != None
    assert res.data['timestamp'] == 1665176140
