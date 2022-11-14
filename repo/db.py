from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import NoResultFound
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

def getRevInfoByRevId(revid):
    session = Session(engine())
    try:
        return session.scalars(select(Revision).where(Revision.rev == revid)).one()
    except NoResultFound:
        return Revision()
def getRevInfosByIds(revIds):
    result =[]
    for i in revIds:
        revInfo =getRevInfoByRevId(i)
        if(revInfo !=None):
            result.append(revInfo.dict())
    return result

def getRevIdsForFile(name):
    with engine().connect() as conn:
        result = conn.execute(
            text("SELECT distinct rev FROM changed_files WHERE origin = :name"),
            {"name": name}
        )
        revIds = []
        for item in result:
            revIds.append(item.rev)
    return revIds


def getRevInfosForFile(name):
    revIds = getRevIdsForFile(name)
    result = getRevInfosByIds(revIds)
    return result


def _getFiles(cmode):
    with engine().connect() as conn:
        result = conn.execute(
            text("SELECT origin,rev,target,id FROM changed_files WHERE cmode = :mode  GROUP BY origin ORDER BY rev"),
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
        ret ={"id":str(i.id), "rev":i.rev,"origin":i.origin,"target":str(i.target)}
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
