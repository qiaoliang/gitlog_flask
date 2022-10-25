import unittest
from app import app
from parser import logParser


class LogParseTestCase(unittest.TestCase):
    def test_parse(self):
        inputs=[
            "Revision: 175c40a\n",
            "###解析 git log 。通过路由 /logfile，将文件内容回写到浏览器。\n",
            ">>>>Detail:\n",
            "<<<<End\n",
            "\n",
            "M	1.txt\n",
            "R100	Dockerfile	app/Dockerfile\n",
            "A	app/__init__.py\n",
            "R077	app.py	app/app.py\n",
            "A	app/parser/__init__.py\n",
            "D	app/parser/logParser.py\n"
        ]
        result = logParser.parse(inputs)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0].rev, "175c40a")
        changes =result[0].changedfiles
        self.assertEqual(len(changes),6)
        # self.assertEqual(changes[0].cmode,"M")