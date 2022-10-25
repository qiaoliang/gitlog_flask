from sqlalchemy import  create_engine,select,text
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.pool import StaticPool

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

def getAllRevInfo():
    session = Session(engine())
    return session.scalars(select(Revision)).all()

def _getFiles(cmode):
    with engine().connect() as conn:
        result = conn.execute(
                text("SELECT distinct origin FROM changed_files WHERE cmode = :mode"),
                {"mode": cmode}
            )
        files=[]
        for item in result:
            files.append(item)
    return files
def tranformToFiles(dbret):
    result = []
    for i in dbret:
        result.append(i.origin)
    return result

def getAppendedFiles():
    return tranformToFiles(_getFiles("A"))
def getModifiedFiles():
    return tranformToFiles(_getFiles("M"))
def getDeletedFiles():
    return tranformToFiles(_getFiles("D"))
def getRenamedFiles():
    return tranformToFiles(_getFiles("R"))
def getAllRevId():
    revInfo = getAllRevInfo()
    result =[]
    for i in revInfo:
        result.append(i.rev)
    return result 