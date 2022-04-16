from multiprocessing.connection import Connection
from sqlalchemy.orm import Session

from iracelog_service_manager.persistence.access import read_events, read_wamp_data
from iracelog_service_manager.persistence.service import session_read_wamp_data_with_diff
from iracelog_service_manager.persistence.util import  orm_session
from iracelog_service_manager.db.schema import Event, WampData


# Tests for get event states (wampdata) with delta

empty = {'cars': [], 'session': []}
sample1 = {'cars': [["A",1], ["B",2]], 'session': [1,2,3]}
sample2 = {'cars': [["A",10], ["Bx",20]], 'session': [7,8,9]}

def test_standard_delta(testOrm:Session):
    """verify the deltas are resolved correct (sample1 vs sample2)"""
    # prepare Event and track
    e = Event(id=1, name="Hallo")
    testOrm.add(e)

    testOrm.add(WampData(eventId=e.id, data={'type':1, 'timestamp': 2, 'payload': sample1}))
    testOrm.add(WampData(eventId=e.id, data={'type':1, 'timestamp': 3, 'payload': sample2}))
    

    # we need the data to be persisted now (otherwise data seems to be not available for next call)
    testOrm.commit()

    # execute
    unwrapped = session_read_wamp_data_with_diff.__wrapped__    
    con = testOrm.get_bind()
    result = unwrapped(con, e.id, 1, 10)    
    
    # check
    
    assert result[0]['type'] == 1
    assert result[0]['payload'] == sample1 # no delta
    assert result[1]['type'] == 8
    assert result[1]['payload']['cars'] == [[0, 1, 10], [1, 0, "Bx"], [1, 1, 20]]
    assert result[1]['payload']['session'] == [[0,7], [1,8], [2,9]]
    

def test_empty_to_filled(testOrm:Session):
    """verify the deltas are resolved correct (empty vs sample1)"""
    # prepare Event and track
    e = Event(id=1, name="Hallo")
    testOrm.add(e)

    testOrm.add(WampData(eventId=e.id, data={'type':1, 'timestamp': 2, 'payload': empty}))
    testOrm.add(WampData(eventId=e.id, data={'type':1, 'timestamp': 3, 'payload': sample1}))
    

    # we need the data to be persisted now (otherwise data seems to be not available for next call)
    testOrm.commit()

    # execute
    unwrapped = session_read_wamp_data_with_diff.__wrapped__    
    con = testOrm.get_bind()
    result = unwrapped(con, e.id, 1, 10)    
    
    # check
    
    assert result[0]['type'] == 1
    assert result[0]['payload'] == empty # no delta
    assert result[1]['type'] == 8
    assert result[1]['payload']['cars'] == [[0, 0, "A"], [0, 1, 1], [1, 0, "B"], [1, 1, 2]]
    assert result[1]['payload']['session'] == [[0,1], [1,2], [2,3]]
    
def test_no_data_within_range(testOrm:Session):
    """verify empty result if no data is in range"""
    # prepare Event and track
    e = Event(id=1, name="Hallo")
    testOrm.add(e)

    testOrm.add(WampData(eventId=e.id, data={'type':1, 'timestamp': 2, 'payload': empty}))
    testOrm.add(WampData(eventId=e.id, data={'type':1, 'timestamp': 3, 'payload': sample1}))
    

    # we need the data to be persisted now (otherwise data seems to be not available for next call)
    testOrm.commit()

    # execute
    unwrapped = session_read_wamp_data_with_diff.__wrapped__    
    con = testOrm.get_bind()
    result = unwrapped(con, e.id, 4, 10)    
    
    # check
    
    assert result == []

def test_only_one_whithin_range(testOrm:Session):
    """verify single result if only one item is in range"""
    # prepare Event and track
    e = Event(id=1, name="Hallo")
    testOrm.add(e)

    
    testOrm.add(WampData(eventId=e.id, data={'type':1, 'timestamp': 3, 'payload': sample1}))
    

    # we need the data to be persisted now (otherwise data seems to be not available for next call)
    testOrm.commit()

    # execute
    unwrapped = session_read_wamp_data_with_diff.__wrapped__    
    con = testOrm.get_bind()
    result = unwrapped(con, e.id, 2, 10)    
    
    # check
    
    assert len(result) == 1
    assert result[0]['type'] == 1
    assert result[0]['payload'] == sample1
    
    

    




