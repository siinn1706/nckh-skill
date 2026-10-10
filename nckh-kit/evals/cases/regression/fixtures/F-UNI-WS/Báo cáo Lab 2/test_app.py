import unittest
from app import authorize, conversion

class Regression(unittest.TestCase):
    def test_denominator(self):
        self.assertEqual(conversion(12, 30), 40)
    def test_not_constant(self):
        self.assertEqual(conversion(6, 30), 20)
    def test_authorization(self):
        self.assertFalse(authorize("alice", "bob"))
        self.assertTrue(authorize("alice", "alice"))

if __name__ == "__main__":
    unittest.main()
