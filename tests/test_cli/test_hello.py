import requests
import unittest

class HelloTestCase(unittest.TestCase):
    def test_index(self):
        res = requests.get("http://localhost:5000")
        assert res.status_code == 200
        self.assertEqual(res.content.decode("utf-8"), "Index Page")
        
    def test_hello(self):
        res = requests.get("http://localhost:5000/hello")
        self.assertEqual(res.content.decode("utf-8"), "<h1>Hello, World!</h1>")