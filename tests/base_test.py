import unittest
from dotenv import load_dotenv
from pathlib import Path
import os

class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        basedir = Path(__file__).parent.absolute() / ".." / "test-data"
        cls.write_env_file(basedir, "test.env")
        load_dotenv(os.path.join(basedir, 'test.env'))

    @classmethod
    def write_env_file(cls, basedir, file):
        with open(basedir / file, "w") as f:
            f.write("CONFIG_PATH=" + (basedir / 'conf').__str__() + "\n")
            f.write("LOG_PATH=" + (basedir / 'logs').__str__())


if __name__ == '__main__':
    unittest.main()
