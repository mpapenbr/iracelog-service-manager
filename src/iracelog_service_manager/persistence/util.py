"""collection of methods for handling the database access"""

import functools
import os

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connection
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import sessionmaker

ENV_DB_URL="DB_URL"



def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class DbHandler():
    def __init__(self) -> None:
        self.eng = create_engine(os.environ.get(ENV_DB_URL), pool_pre_ping=True, echo_pool=True)
        
    def new_session(self):
        return Session(self.eng)
        
       

def db_connector(func) -> Connection:
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        with DbHandler().eng.connect():
            return func(args,kwargs)


def orm_session() -> Session:
    with DbHandler().eng.connect() as con:
        dbSession = Session(bind=con)
        yield dbSession


def tx(func) -> Session:
    """
    wraps the function in a transaction.
    The transaction is committed if there are no exceptions.
    Otherwise a rollback will be initiated
    """
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        with DbHandler().eng.connect() as con:
            dbSession = Session(bind=con)
            dbSession.begin()
            try:
                ret = func(dbSession, *args,**kwargs)
                dbSession.commit();
                return ret;
            except Exception as e:
                dbSession.rollback()
                raise e
    return _wrapper

