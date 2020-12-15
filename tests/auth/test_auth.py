import unittest
from tests.base_api_test import BaseApiTest


class AuthTest(BaseApiTest):

    def test_login(self):
        json = dict(
            email="admin",
            password="admin"
        )
        rv = self.client.post('/api/login', json=json)
        print(rv)
        self.assertEqual("admin", rv.get_json().get("email"))
        self.assertEqual(1, rv.get_json().get("id"))

    def test_login_bad_user(self):
        json = dict(
            email="test",
            password="admin"
        )
        rv = self.client.post('/api/login', json=json)
        self.assertFalse(rv.get_json().get("authenticated"))
        self.assertEqual("Invalid credentials", rv.get_json().get("message"))

    def test_login_bad_password(self):
        json = dict(
            email="admin",
            password="other"
        )
        rv = self.client.post('/api/login', json=json)
        self.assertFalse(rv.get_json().get("authenticated"))
        self.assertEqual("Invalid credentials", rv.get_json().get("message"))


if __name__ == '__main__':
    unittest.main()
