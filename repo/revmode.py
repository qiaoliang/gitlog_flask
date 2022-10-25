
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
class Revision(Base):
    __tablename__ = "revision_infos"

    id = Column(Integer, primary_key=True)
    rev = Column(String(30))
    brief = Column(String)
    detail = Column(String)
    changedfiles = relationship(
         "ChangedFile", back_populates="revision", cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"Revision(id={self.id!r}, rev={self.rev!r}, brief={self.brief!r})"

    def setRev(self,r):
        self.rev=r
    def setBrief(self,b):
        self.brief = b
    def addDetail(self,d):
        if(self.detail is None):
            self.detail=""
        self.detail = self.detail + d; 
    def addChange(self,c):
        self.changedfiles.append(c)

    def toDict(self):
        result= {'inst':self.id,'rev':self.rev, 'brief':self.brief, 'detail':self.detail}
        changes =[]
        for f_item in self.changedfiles:
            changes.append(f_item.toDict())
        result['changedfiles'] = changes
        return result 
class ChangedFile(Base):
    __tablename__ = "changed_files"

    id = Column(Integer, primary_key=True)
    cmode = Column(String(30))
    origin = Column(String)
    target = Column(String)
    revid = Column(String, ForeignKey("revision_infos.rev"), nullable=False)
    revision = relationship("Revision", back_populates="changedfiles")
    def __repr__(self):
        return f"ChangedFile(id={self.id!r}, revid={self.revid!r}, cmode={self.cmode!r},origin={self.origin!r},target={self.origin!r})"
    def toDict(self):
        return {'instid':self.id,'cmode':self.cmode, 'origin':self.origin, 'target':self.target,'revid':self.revid}
    @staticmethod
    def create(str):
        cfile = ChangedFile()
        items=str.split('\t')
        length = len(items)
        if(length >= 2):
            cfile.cmode = items[0][0:1]
            cfile.origin = items[1]
        if(length==3):
            cfile.target = items[2]
        return cfile
