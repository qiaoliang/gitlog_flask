import unittest
from app import app
from repo import revmode


class RevModeTestCase(unittest.TestCase):
    def test_ChangedFile(self):
        line = "M	1.txt"
        result = revmode.ChangedFile.create(line)
        self.assertEqual(result.cmode,"M")
        self.assertEqual(result.origin,"1.txt")