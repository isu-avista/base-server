import unittest
from avista_base.service import Service
from flask import Flask
from avista_base.service_status import ServiceStatus
from dotenv import load_dotenv
from pathlib import Path
import os


class ServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.chdir("..")
        basedir = Path(os.getcwd()) / "test-data"
        cls.write_env_file(basedir, "test.env")
        load_dotenv(os.path.join(basedir, 'test.env'))

    @classmethod
    def write_env_file(cls, basedir, file):
        with open(basedir / file, "w") as f:
            f.write("CONFIG_PATH=" + basedir.__str__())

    def setUp(self):
        app = Flask("Test")
        self.service = Service(app, "Test")

    def test_init(self):
        self.service.init()
        self.assertEqual(ServiceStatus.INITIALIZING, self.service.status())

    def test_start(self):
        self.service.start()
        self.assertEqual(ServiceStatus.RUNNING, self.service.status())

    def test_run(self):
        self.service.run()
        self.assertEqual(ServiceStatus.RUNNING, self.service.status())

    def test_restart(self):
        self.service.restart()
        self.assertEqual(ServiceStatus.RUNNING, self.service.status())

    def test_stop(self):
        self.service.stop()
        self.assertEqual(ServiceStatus.IDLE, self.service.status())

    def test_status(self):
        self.assertEqual(ServiceStatus.IDLE, self.service.status())


if __name__ == '__main__':
    unittest.main()
