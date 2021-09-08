import unittest
from main import main


class TestIPFound(unittest.TestCase):

    def test_from_doc(self):
        self.assertEqual(main("D:\\ipv4", "4"), "192.168.0.0/23")

    def test_new_data(self):
        self.assertEqual(main("D:\\ipv41", "4"), "192.168.0.0/25")
        self.assertEqual(main("D:\\ipv42", "4"), "192.168.0.0/23")
        self.assertEqual(main("D:\\ipv46", "4"), "0.0.0.0/0")
        self.assertEqual(main("D:\\ipv48", "4"), "192.168.1.0/27")

    def test_error(self):
        self.assertRaises(ValueError, main, "D:\\ipv43", "4")
        self.assertRaises(ValueError, main, "D:\\ipv44", "4")
        self.assertRaises(ValueError, main, "D:\\ipv45", "4")
        self.assertRaises(ValueError, main, "D:\\ipv47", "4")
