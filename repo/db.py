from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from repo.revmode import Revision

# using memory db
_engine = create_engine("sqlite:///:memory:", poolclass=StaticPool,
                        connect_args={'check_same_thread': False})


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


def getAllRevInfo():
    session = Session(engine())
    return session.scalars(select(Revision)).all()


def getRevIdsForFile(name):
    with engine().connect() as conn:
        result = conn.execute(
            text("SELECT distinct revid FROM changed_files WHERE origin = :name"),
            {"name": name}
        )
        revIds = []
        for item in result:
            revIds.append(item.revid)
    return revIds


def getRevInfosByIds(revIds):
    session = Session(engine())
    result =[]
    for i in revIds:
        stmt = select(Revision).where(Revision.rev == i)
        revInfo =session.scalars(stmt).one()
        if(revInfo !=None):
            result.append(revInfo)
    return result

def getRevInfosForFile(name):
    revIds = getRevIdsForFile(name)
    result = getRevInfosByIds(revIds)
    return result


def _getFiles(cmode):
    with engine().connect() as conn:
        result = conn.execute(
            text("SELECT origin,revid,target,id FROM changed_files WHERE cmode = :mode  GROUP BY origin ORDER BY revid"),
            {"mode": cmode}
        )
        files = []
        for item in result:
            print(item)
            files.append(item)
    return files


def rowToFiles(dbret):
    result = []
    for i in dbret:
        ret ={"id":str(i.id), "rev":i.revid,"origin":i.origin,"target":str(i.target)}
        result.append(ret)
    return result


def getAppendedFiles():
    return rowToFiles(_getFiles("A"))


def getModifiedFiles():
    return rowToFiles(_getFiles("M"))


def getDeletedFiles():
    return rowToFiles(_getFiles("D"))


def getRenamedFiles():
    return rowToFiles(_getFiles("R"))


def getAllRevId():
    revInfo = getAllRevInfo()
    result = []
    for i in revInfo:
        result.append(i.rev)
    return result
