import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main


class TestTracker(unittest.TestCase):
    def test_add_list_status_count(self):
        with tempfile.TemporaryDirectory() as d:
            db = os.path.join(d, "c.csv")
            self.assertEqual(main.add(db, "Upgrade Wi-Fi", "ali"), "CR-001")
            main.add(db, "Replace switch", "bob")
            main.set_status(db, "CR-001", "done")
            self.assertEqual(main.counts(db)["done"], 1)
            self.assertEqual(main.counts(db)["open"], 1)
            self.assertEqual(len(main.list_all(db)), 2)

    def test_bad_status_raises(self):
        with tempfile.TemporaryDirectory() as d:
            db = os.path.join(d, "c.csv")
            main.add(db, "T", "ali")
            with self.assertRaises(ValueError):
                main.set_status(db, "CR-001", "weird")


if __name__ == "__main__":
    unittest.main()
