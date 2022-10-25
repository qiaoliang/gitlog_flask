from sqlalchemy import  create_engine,select
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.pool import StaticPool
from parser import logParser

from repo.revmode import Revision

# using memory db
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

def getAllRevInfo():
    session = Session(engine())
    return session.scalars(select(Revision)).all()

def getAllRevId():
    revInfo = getAllRevInfo()
    result =[]
    for i in revInfo:
        result.append(i.rev)
    return result