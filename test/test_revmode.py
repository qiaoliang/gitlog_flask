import unittest
from repo import revmode
from parser import logParser

_revInfo_with_changes_text = [
    "Revision: 175c40a\n",
    "###IamBrief\n",
    "<<<<Detail:\n",
    "\n",
    "i am Detail 1\n",
    "<<<<End\n",
    "\n",
    "M	1.txt\n",
    "R100	Dockerfile	app/Dockerfile\n",
]


class RevModeTestCase(unittest.TestCase):
    maxDiff = None

    def test_create_a_modified_files(self):
        line = "M	1.txt"
        result = revmode.ChangedFile.create(line)
        self.assertEqual(result.cmode, "M")
        self.assertEqual(result.origin, "1.txt")
        self.assertEqual(result.target, None)

    def test_create_a_deleted_files(self):
        line = "D	app/parser/logParser.py"
        result = revmode.ChangedFile.create(line)
        self.assertEqual(result.cmode, "D")
        self.assertEqual(result.origin, "app/parser/logParser.py")
        self.assertEqual(result.target, None)

    def test_create_a_Renamed_files(self):
        line = "R100	Dockerfile	app/Dockerfile"
        result = revmode.ChangedFile.create(line)
        self.assertEqual(result.cmode, 'R')
        self.assertEqual(result.origin, "Dockerfile")
        self.assertEqual(result.target, "app/Dockerfile")

    def test_create_a_Renamed_files(self):
        line = "A	1.txt"
        result = revmode.ChangedFile.create(line)
        self.assertEqual(result.cmode, 'A')
        self.assertEqual(result.origin, "1.txt")
        self.assertEqual(result.target, None)

    def test_Changed_file_to_dict(self):
        modified_file = revmode.ChangedFile.create("M	1.txt")
        modified_file.rev = '4527ss5223'
        modified_file.id = 1
        expect1 = {'cmode': 'M', 'origin': '1.txt',
                   'target': None, 'id': 1, 'rev': '4527ss5223'}
        self.assertEqual(expect1, modified_file.dict())

        renamed_file = revmode.ChangedFile.create(
            "R100	Dockerfile	app/Dockerfile")
        renamed_file.rev = '23232323'
        renamed_file.id = 2
        expect2 = {'cmode': 'R', 'origin': 'Dockerfile',
                   'target': 'app/Dockerfile', 'id': 2, 'rev': '23232323'}
        self.assertEqual(expect2, renamed_file.dict())

    def test_RevisionInfo_to_dict(self):
        result = logParser.parse(_revInfo_with_changes_text)
        expected = {'id': None, 'rev': '175c40a', 'brief': 'IamBrief', 'detail': '\ni am Detail 1\n',
                    'changes': [
                        {'cmode': 'M', 'origin': '1.txt', 'target': None,
                            'id': None, 'rev': '175c40a'},
                        {'cmode': 'R', 'origin': 'Dockerfile',
                            'target': 'app/Dockerfile', 'id': None, 'rev': '175c40a'},
                    ]
                    }
        self.assertEqual(expected, result[0].dict())

    def ChangedFile(self, cmode="M", origin="1.txt", target=None, rev="This_REV_ID", id=0):
        afile = revmode.ChangedFile()
        afile.cmode = cmode
        afile.origin = origin
        afile.target = target
        afile.rev = rev
        afile.id = id
        return afile


class FileBuilder(object):
    @staticmethod
    def newInstance():
        builder = FileBuilder()
        builder._cmode = "M"
        builder._origin = "origin.txt"
        builder._target = None
        builder._revid = "DEFULT_REV"
        builder._id = 0
        return builder

    def cmode(self, cmode):
        self._cmode = cmode
        return self

    def origin(self, origin):
        self._origin = origin
        return self

    def target(self, target):
        self._target = target
        return self

    def rev(self, rev_id):
        self._rev = rev_id
        return self

    def id(self, id):
        self._id = id
        return self

    def build(self):
        afile = revmode.ChangedFile()
        afile.id = self._id
        afile.cmode = self._cmode
        afile.origin = self._origin
        afile.target = self._target
        afile.rev = self._rev
        return afile


class RevBuilder(object):
    @staticmethod
    def newInstance():
        builder = RevBuilder()
        builder = revmode.Revision()
        builder._rev = "REV_ID"
        builder._id= 0
        builder._brief="IamBrief"
        builder._detail= "I am 1st Line in Detail\n I am 2rd Line in Detail"
        builder._changs = []
        return builder

    def rev(self, rev):
        self._rev = rev
        return self

    def brief(self, b):
        self._brief = b
        return self

    def detail(self, d):
        self._detail = d
        return self

    def id(self, id):
        self._id = id
        return self

    def addFile(self, c):
        if(self._changes == None ):
            self._changes =[]
        if(c!= None and type(c)== revmode.ChangedFile):
            c.rev = self._rev
            c.id = self._changes.len()
            self._changes.append(c)
        return self

    def addFiles(self, c):
        if(c== None or not isinstance(c,list)):
            return self
        for item in c:
            if(type(item)==  revmode.ChangedFile):
                self.addFile(item)
        return self

    def build(self):
        rev = revmode.Revision()
        rev.id = self._id
        rev.rev = self._rev
        rev.brief = self._brief
        rev.detail = self._detail
        rev.changes = self._changes
        return rev
