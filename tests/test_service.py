import unittest
from avista_base.service_status import ServiceStatus
from avista_data import db
from tests.mock_service import MockService
from tests.base_test import BaseTest


class ServiceTest(BaseTest):

    def setUp(self):
        self.service = MockService.get_instance()

    def tearDown(self):
        db.drop_all()
        if self.service.status() == ServiceStatus.RUNNING:
            self.service.stop()

    def test_init(self):
        self.service.initialize()
        self.assertEqual(ServiceStatus.INITIALIZING, self.service.status())

    def test_start(self):
        self.service.start()
        self.assertEqual(ServiceStatus.RUNNING, self.service.status())

    def test_restart(self):
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
