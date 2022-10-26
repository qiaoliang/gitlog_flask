import unittest
from app import app
from parser import logParser

_log_2_rev=[
    "Revision: 175c40a\n",
    "Revision: 234561a\n",
]
_logtext_1_rev=[
    "Revision: 175c40a\n",
    "###解析 git log 。通过路由 /logfile，将文件内容回写到浏览器。\n",
    "<<<<Detail:\n",
    "\n",
    "i am Detail 1\n",
    "i am Detail 2 Text\n",
    "<<<<End\n",
    "\n",
    "M	1.txt\n",
    "R100	Dockerfile	app/Dockerfile\n",
    "A	app/__init__.py\n",
    "R077	app.py	app/app.py\n",
    "A	app/parser/__init__.py\n",
    "D	app/parser/logParser.py\n"
]

class LogParseTestCase(unittest.TestCase):
    def test_parse(self):
        result = logParser.parse(_logtext_1_rev)
        self.assertEqual(len(result),1)
        revInfo =result[0] 
        self.assertEqual(revInfo.rev, "175c40a")
        self.assertEqual(revInfo.brief,"解析 git log 。通过路由 /logfile，将文件内容回写到浏览器。")
        self.assertEqual(revInfo.detail,"\ni am Detail 1\ni am Detail 2 Text\n")
 
        changes =revInfo.changedfiles
        self.assertEqual(len(changes),6)
        self.assertEqual(changes[3].cmode,"R")
        self.assertEqual(changes[3].origin,"app.py")
        self.assertEqual(changes[3].target,"app/app.py")



    def test_should_has_two_revisionse(self):
        result = logParser.parse(_log_2_rev)
        self.assertEqual(len(result),2)
        self.assertEqual(result[0].rev, "175c40a")
        self.assertEqual(result[1].rev, "234561a")

