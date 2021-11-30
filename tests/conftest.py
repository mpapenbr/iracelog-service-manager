from sqlalchemy import event
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
import pytest
import os
from sqlalchemy.orm import Session




@pytest.fixture(scope="module")
def testOrmX():
    eng = create_engine(os.environ.get("TEST_DB_URL"))    
    with eng.connect() as con:
        ormSession = Session(bind=con)
        yield ormSession

@pytest.fixture(scope="session")
def connection():
    engine = create_engine(os.environ.get("TEST_DB_URL"))    
    connection = engine.connect()

    yield connection

    connection.close()
        

@pytest.fixture(autouse=True)
def testOrm(connection):
    """Returns a database session to be used in a test.

    This fixture also alters the application's database
    connection to run in a transactional fashion. This means
    that all tests will run within a transaction, all database
    operations will be rolled back at the end of each test,
    and no test data will be persisted after each test.

    `autouse=True` is used so that session is properly
    initialized at the beginning of the test suite and
    factories can use it automatically.
    """
    transaction = connection.begin()
    session = Session(bind=connection)
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(db_session, transaction):
        """Support tests with rollbacks.

        This is required for tests that call some services that issue
        rollbacks in try-except blocks.

        With this event the Session always runs all operations within
        the scope of a SAVEPOINT, which is established at the start of
        each transaction, so that tests can also rollback the
        “transaction” as well while still remaining in the scope of a
        larger “transaction” that’s never committed.
        """
        if transaction.nested and not transaction._parent.nested:
            # ensure that state is expired the way session.commit() at
            # the top level normally does
            session.expire_all()
            session.begin_nested()

    yield session

    session.close()
    transaction.rollback()

        
