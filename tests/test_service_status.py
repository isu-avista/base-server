import unittest
from avista_base.service_status import ServiceStatus


class ServiceStatusTest(unittest.TestCase):

    def test_from_str(self):
        oracle = [
            ["IDLE", ServiceStatus.IDLE],
            ["idle", ServiceStatus.IDLE],
            ["Idle", ServiceStatus.IDLE],
            ["STARTING", ServiceStatus.STARTING],
            ["starting", ServiceStatus.STARTING],
            ["Starting", ServiceStatus.STARTING],
            ["INITIALIZING", ServiceStatus.INITIALIZING],
            ["initializing", ServiceStatus.INITIALIZING],
            ["Initializing", ServiceStatus.INITIALIZING],
            ["RUNNING", ServiceStatus.RUNNING],
            ["running", ServiceStatus.RUNNING],
            ["Running", ServiceStatus.RUNNING],
            ["STOPPING", ServiceStatus.STOPPING],
            ["stopping", ServiceStatus.STOPPING],
            ["Stopping", ServiceStatus.STOPPING],
            ["ERROR", ServiceStatus.ERROR],
            ["error", ServiceStatus.ERROR],
            ["Error", ServiceStatus.ERROR]
        ]
        for x in range(len(oracle)):
            self.assertEqual(oracle[x][1], ServiceStatus.from_str(oracle[x][0]))

    def test_invalid_str(self):
        with self.assertRaises(NotImplementedError):
            ServiceStatus.from_str("Test")

    def test_none(self):
        with self.assertRaises(NotImplementedError):
            ServiceStatus.from_str(None)

    def test_repr(self):
        self.assertEqual("Service Status: IDLE", ServiceStatus.IDLE.__repr__(), "repr not same")

    def test_str(self):
        self.assertEqual("Idle", str(ServiceStatus.IDLE), "string representation not same")


if __name__ == '__main__':
    unittest.main()
