import unittest
from tests.base_api_test import BaseApiTest
from avista_data.user import User
from avista_data.role import Role


class UserTest(BaseApiTest):

    def setUp(self):
        super().setUp()
        self.user = User()
        self.user.set_first_name("Foo")
        self.user.set_last_name("Bar")
        self.user.set_role(Role.USER)
        self.user.set_email("foo@bar.com")
        self.user.set_password("password")
        print("app:", self.server._app)
        print("app.session", self.server._app.session)
        self.server._app.session.add(self.user)
        self.server._app.session.commit()

    def test_create_user(self):
        json = dict(
            first_name="FooFoo",
            last_name="BarBar",
            role="USER",
            email="foofoo@barbar.com",
            password="passowrd",
        )
        rv = BaseApiTest.auth_post(self.client, "admin", "admin", route="/api/users", json=json)
        self.assertEqual("User added!", rv.get_json().get('message'))
        self.assertEqual("success", rv.get_json().get('status'))

    def test_create_user_noauth(self):
        json = dict(
            first_name="FooFoo",
            last_name="BarBar",
            role="USER",
            email="foofoo@barbar.com",
            password="passowrd",
        )
        rv = self.client.post('/api/users', json=json)
        self.assertEqual('Missing Authorization Header', rv.get_json().get('msg'))

    def test_create_user_auth_nodata(self):
        json = dict()
        rv = BaseApiTest.auth_post(self.client, "admin", "admin", route="/api/users", json=json)
        self.assertEqual("Missing data", rv.get_json().get('message'))
        self.assertEqual('failure', rv.get_json().get('status'))
        self.assertEqual("400 BAD REQUEST", rv.status)

    def test_create_user_auth_nonjson(self):
        json = dict()
        rv = self.client.post('/api/users', data=json, headers=BaseApiTest._create_auth_header(self.client, "admin", "admin"))
        self.assertEqual("Missing JSON in request", rv.get_json().get('msg'))

    def test_read_all_users(self):
        rv = BaseApiTest.auth_get(self.client, "admin", "admin", route="/api/users")
        self.assertEqual(2, len(rv.get_json()))

    def test_read_all_users_noauth(self):
        rv = self.client.get('/api/users')
        self.assertEqual('Missing Authorization Header', rv.get_json().get('msg'))

    def test_read_one_user(self):
        rv = BaseApiTest.auth_get(self.client, "admin", "admin", route=f"/api/users/{self.user.get_id()}")
        self.assertEqual(self.user.get_id(), rv.get_json().get("id"))
        self.assertEqual(self.user.get_email(), rv.get_json().get("email"))

    def test_read_one_user_noauth(self):
        rv = self.client.get(f'/api/users/{self.user.get_id()}')
        self.assertEqual('Missing Authorization Header', rv.get_json().get('msg'))

    # def test_read_one_user_notself_notadmin(self):
    #     rv = BaseApiTest.auth_get(self.client, "foo@bar.com", "password", route=f"/api/users/{self.user.get_id()}")
    #     self.fail()

    def test_read_one_user_self_notadmin(self):
        rv = BaseApiTest.auth_get(self.client, "foo@bar.com", "password", route=f"/api/users/{self.user.get_id()}")
        self.assertEqual(self.user.get_id(), rv.get_json().get("id"))
        self.assertEqual(self.user.get_email(), rv.get_json().get("email"))

    def test_read_one_user_self_admin(self):
        rv = BaseApiTest.auth_get(self.client, "admin", "admin", route="/api/users/1")
        self.assertEqual(1, rv.get_json().get("id"))
        self.assertEqual("admin", rv.get_json().get("email"))

    # def test_update_user(self):
    #     json = dict()
    #     rv = BaseApiTest.auth_put(self.client, "admin", "admin", route="/api/users/1", json=json)
    #     self.fail()
    #
    # def test_update_user_noauth(self):
    #     json = dict()
    #     rv = BaseApiTest.auth_put(self.client, "admin", "admin", route="/api/users/1", json=json)
    #     self.fail()
    #
    # def test_update_user_unknown(self):
    #     json = dict()
    #     rv = BaseApiTest.auth_put(self.client, "admin", "admin", route="/api/users/1", json=json)
    #     self.fail()
    #
    # def test_update_user_known_auth_nodata(self):
    #     json = dict()
    #     rv = BaseApiTest.auth_put(self.client, "admin", "admin", route="/api/users/1", json=json)
    #     self.fail()
    #
    # def test_update_user_known_auth_nonjson(self):
    #     json = dict()
    #     rv = BaseApiTest.auth_put(self.client, "admin", "admin", route="/api/users/1", json=json)
    #     self.fail()
    #
    # def test_delete_user(self):
    #     rv = BaseApiTest.auth_delete(self.client, "admin", "admin", route="/api/users/1")
    #     self.fail()
    #
    # def test_delete_user_noauth(self):
    #     rv = BaseApiTest.auth_delete(self.client, "admin", "admin", route="/api/users/1")
    #     self.fail()
    #
    # def test_delete_user_noadmin(self):
    #     rv = BaseApiTest.auth_delete(self.client, "admin", "admin", route="/api/users/1")
    #     self.fail()
    #
    # def test_delete_user_unknown(self):
    #     rv = BaseApiTest.auth_delete(self.client, "admin", "admin", route="/api/users/1")
    #     self.fail()


if __name__ == '__main__':
    unittest.main()
