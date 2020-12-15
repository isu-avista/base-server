import unittest
from avista_base.service_status import ServiceStatus
from dotenv import load_dotenv
from pathlib import Path
from avista_data import db
import os
from tests.mock_service import MockService


class ServiceTest(unittest.TestCase):

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

    def setUp(self):
        self.service = MockService.get_instance()

    def tearDown(self):
        db.drop_all()
        if self.service.status() == ServiceStatus.RUNNING:
            self.service.stop()

    def test_init(self):
        self.service.init()
        self.assertEqual(ServiceStatus.INITIALIZING, self.service.status())

    def test_start(self):
        self.service.start()
        self.assertEqual(ServiceStatus.RUNNING, self.service.status())

    def test_restart(self):
        self.service.init()
        self.service.start()
        self.service.restart()
        self.assertEqual(ServiceStatus.RUNNING, self.service.status())

    def test_stop(self):
        self.service.stop()
        self.assertEqual(ServiceStatus.IDLE, self.service.status())

    def test_status(self):
        self.assertEqual(ServiceStatus.IDLE, self.service.status())


if __name__ == '__main__':
    unittest.main()
