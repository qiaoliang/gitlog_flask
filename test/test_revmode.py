import unittest
from app import app
from repo import revmode


class RevModeTestCase(unittest.TestCase):
    def test_parse_modified_files(self):
        line = "M	1.txt"
        result = revmode.ChangedFile.create(line)
        self.assertEqual(result.cmode,"M")
        self.assertEqual(result.origin,"1.txt")
        self.assertEqual(result.target,None)

    def test_parse_deleted_files(self):
        line = "D	app/parser/logParser.py"
        result = revmode.ChangedFile.create(line)
        self.assertEqual(result.cmode,"D")
        self.assertEqual(result.origin,"app/parser/logParser.py")
        self.assertEqual(result.target,None)

    def test_parse_Renamed_files(self):
        line = "R100	Dockerfile	app/Dockerfile"
        result = revmode.ChangedFile.create(line)
        self.assertEqual(result.cmode,'R')
        self.assertEqual(result.origin,"Dockerfile")
        self.assertEqual(result.target,"app/Dockerfile")