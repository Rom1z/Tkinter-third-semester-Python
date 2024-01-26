import unittest

from add import add_test


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(add_test(), 12)


if __name__ == '__main__':
    unittest.main()
