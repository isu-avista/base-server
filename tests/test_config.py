import unittest
from avista_base import config
import os
from pathlib import Path


class ConfigTest(unittest.TestCase):

    file = ""
    basedir = ""

    @classmethod
    def setUpClass(cls):
        while not os.path.isdir("./test-data"):
            os.chdir("..")

    def setUp(self):
        self.basedir = Path(os.getcwd())
        self.file = self.basedir / "test-data" / "config.yml"

    def test_save(self):
        data = {"test": "test2"}
        newfile = self.basedir / "test-data" / "config2.yml"
        config.save(data, newfile.__str__())
        data = config.load(newfile.__str__())
        self.assertIn("test", data.keys(), "missing key")
        self.assertEqual("test2", data["test"], "value not the same")

    def test_load(self):
        data = config.load(self.file.__str__())
        self.assertIn("test", data.keys(), "missing key")
        self.assertEqual("test", data["test"], "value not the same")


if __name__ == '__main__':
    unittest.main()
