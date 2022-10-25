import unittest
from repo import db
from repo.revmode import Base

class DbTestCase(unittest.TestCase):
    @classmethod
    def setupClass(self):
        Base.metadata.create_all(db.engine())

    def test_getAllRevId(self):
        self.assertEqual(4, len(db.getAllRevId()))


    def test_getAppendedFiles(self):
        self.assertEqual(10, len(db.getAppendedFiles()))


    def test_getRevIdsForFile(self):
        expect = ['d0166fe', '175c40a', 'cf09f40']
        result = db.getRevIdsForFile("1.txt")
        self.assertEqual(3, len(result))
        self.assertTrue(expect == result)

    def test_getRevInfosById(self):
        revids = ['d0166fe', '175c40a', 'cf09f40']
        result = db.getRevInfosByIds(revids)
        self.assertEqual(3, len(result))
