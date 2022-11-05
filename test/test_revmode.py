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
        modified_file.revid = '4527ss5223'
        modified_file.id = 1
        expect1 = {'cmode': 'M', 'origin': '1.txt',
                   'target': None, 'instid': 1, 'revid': '4527ss5223'}
        self.assertEqual(expect1, modified_file.dict())

        renamed_file = revmode.ChangedFile.create(
            "R100	Dockerfile	app/Dockerfile")
        renamed_file.revid = '23232323'
        renamed_file.id = 2
        expect2 = {'cmode': 'R', 'origin': 'Dockerfile',
                   'target': 'app/Dockerfile', 'instid': 2, 'revid': '23232323'}
        self.assertEqual(expect2, renamed_file.dict())

    def test_RevisionInfo_to_dict(self):
        result = logParser.parse(_revInfo_with_changes_text)
        expected= {'instid':None,'rev':'175c40a', 'brief':'IamBrief', 'detail':'\ni am Detail 1\n',
                    'changedfiles':[
                        {'cmode': 'M', 'origin': '1.txt','target': None, 'instid': None, 'revid': '175c40a'},
                        {'cmode': 'R', 'origin': 'Dockerfile','target': 'app/Dockerfile', 'instid': None, 'revid': '175c40a'},
                    ]
                }
        self.assertEqual(expected, result[0].dict())

    def ChangedFile(self,cmode = "M",origin="1.txt",target=None,rev="This_REV_ID",id=0):
            afile = revmode.ChangedFile()
            afile.cmode = cmode
            afile.origin = origin
            afile.target = target
            afile.revid = rev
            afile.id = id
            return afile
class CFileBuilder(object):
    @staticmethod
    def newInstance():
        afile = revmode.ChangedFile()
        afile._cmode = "M"
        afile._origin = "origin.txt"
        afile._target = None
        afile._revid = "DEFULT_REV"
        afile._id = 0
        return afile

    def cmode(self,cmode):
        self._cmode = cmode
        return self

    def origin(self,origin):
        self._origin = origin
        return self

    def target(self,target):
        self._target = target
        return self
    def rev(self,rev_id):
        self._revid = rev_id
        return self
    def id(self,id):
        self._id = id
        return self
    def build(self):
        afile = revmode.ChangedFile()
        afile.id = self._id
        afile.cmode = self._cmode
        afile.origin = self._origin
        afile.target = self._target
        afile.revid = self._revid
        return afile