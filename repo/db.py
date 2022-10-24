from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import select
from repo.revmode import Revision, Base
from sqlalchemy.pool import StaticPool
# use memory db
_engine = create_engine("sqlite:///:memory:", poolclass=StaticPool, connect_args={'check_same_thread': False})
def engine():
    return _engine
def session():
    Session = sessionmaker(_engine)
    return Session

def saveRev(ris):
    with session().begin() as mysession:
        for ri in ris:
            mysession.add(ri)
        mysession.commit()
    with session().begin() as mysession:
        stmt = select(Revision)
        for revInfo in mysession.scalars(stmt):
            print(revInfo)
            print(revInfo.changedfiles[0])
def getAllRev():
    with session().begin() as mysession:
        stmt = select(Revision)
        for revInfo in mysession.scalars(stmt):
            print(revInfo)
            print(revInfo.changedfiles[0])
    return "OK"