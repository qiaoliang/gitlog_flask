import unittest
from app import app


class HelloWorldTestCase(unittest.TestCase):
    def test_hello_world(self):
        self.app = app.test_client()
        self.app.testing = True

        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b'Hello World!')
