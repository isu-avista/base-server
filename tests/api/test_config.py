import unittest
from tests.base_api_test import BaseApiTest


class ConfigTest(BaseApiTest):

    def test_read_dbconfig(self):
        rv = BaseApiTest.auth_get(self.client, "admin", "admin", "/api/config/dbdata")
        self.assertEqual(4, len(rv.get_json()))

    def test_read_dbconfig_noauth(self):
        rv = self.client.get("/api/config/dbdata")
        self.assertEqual("Missing Authorization Header", rv.get_json().get("msg"))

    def test_update_dbconfig(self):
        json = dict()
        rv = BaseApiTest.auth_put(self.client, "admin", "admin", route="/api/config/dbdata", json=json)
        print(rv.get_json())
        self.fail()

    def test_update_dbconfig_noauth(self):
        rv = self.client.put("/api/config/dbdata", json=dict())
        self.assertEqual("Missing Authorization Header", rv.get_json().get("msg"))

    def test_update_dbconfig_nojson(self):
        json = dict()
        headers = BaseApiTest._create_auth_header(self.client, "admin", "admin")
        rv = self.client.put("/api/config/dbdata", headers=headers, data=json)
        self.assertEqual("data cannot be None", rv.get_json().get("msg"))

    def test_read_sysconfig(self):
        rv = BaseApiTest.auth_get(self.client, "admin", "admin", "/api/config/sysdata")
        self.assertEqual(5, len(rv.get_json()))

    def test_read_sysconfig_noauth(self):
        rv = self.client.get("/api/config/sysdata")
        self.assertEqual("Missing Authorization Header", rv.get_json().get("msg"))

    def test_update_sysconfig(self):
        json = dict()
        rv = BaseApiTest.auth_put(self.client, "admin", "admin", route="/api/config/sysdata", json=json)
        print(rv.get_json())
        self.fail()

    def test_update_sysconfig_noauth(self):
        rv = self.client.put("/api/config/sysdata", json=dict())
        self.assertEqual("Missing Authorization Header", rv.get_json().get("msg"))

    def test_update_sysconfig_nojson(self):
        json = dict()
        headers = BaseApiTest._create_auth_header(self.client, "admin", "admin")
        rv = self.client.put("/api/config/dbdata", headers=headers, data=json)
        self.assertEqual("data cannot be None", rv.get_json().get("msg"))

    def test_read_unknown_section(self):
        rv = BaseApiTest.auth_get(self.client, "admin", "admin", "/api/config/unknown")
        self.assertEqual("section cannot be None or empty and must be in the config", rv.get_json().get('msg'))

    def test_update_unknown_section(self):
        rv = self.client.get("/api/config/unknown")
        self.assertEqual("Missing Authorization Header", rv.get_json().get("msg"))


if __name__ == '__main__':
    unittest.main()