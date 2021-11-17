from sqlalchemy.orm import Session

from iracelog_service_manager.persistence.access import read_events
from iracelog_service_manager.persistence.util import  orm_session
from iracelog_service_manager.db.schema import Event




def test_read_events(testOrm:Session):
    print(testOrm)
    res = read_events(testOrm)
    print(res)



def test_write_event(testOrm:Session):
    e = Event(name="Hallo")
    testOrm.add(e)
    # testOrm.commit()
    res = read_events(testOrm)
    assert e == res[0]
    assert res[0].name == "Hallo"



