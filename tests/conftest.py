from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
import pytest
import os
from sqlalchemy.orm import Session



@pytest.fixture(scope="module")
def testOrm():
    eng = create_engine(os.environ.get("DB_URL"))    
    with eng.connect() as con:
        ormSession = Session(bind=con)
        yield ormSession
