import unittest

from addtest import add_test

class MyTestCase(unittest.TestCase):
    def test_something0(self):
        self.assertEqual(add_test(),12)
    def test_something1(self):
        self.assertEqual(add_test(),10)
    def test_something2(self):
        self.assertEqual(add_test(),58)
    def test_something3(self):
        self.assertEqual(add_test(),43)

if __name__ == '__main__':
    unittest.main()
