import unittest
from tests.base_test import BaseTest
from tests.mock_service import MockService
import avista_data


class BaseApiTest(BaseTest):

    def setUp(self):
        self.server = MockService.get_instance()
        self.server.initialize()
        self.server.start()
        self.client = self.server._app.test_client()

    def tearDown(self):
        # self.server._app.session.remove()
        avista_data.database.clear_data()
        self.server.stop()

    @staticmethod
    def __login(client, email, password):
        return client.post('/api/login', json=dict(
            email=email,
            password=password
        ))

    @staticmethod
    def _create_auth_header(client, email, password):
        credentials = BaseApiTest.__login(client, email, password)
        print(f'Credentials: {credentials.get_json()}')
        return {
            'Authorization': f'Bearer {credentials.get_json()["token"]}'
        }

    @staticmethod
    def auth_get(client, email, password, route):
        headers = BaseApiTest._create_auth_header(client, email, password)
        return client.get(route, headers=headers)

    @staticmethod
    def auth_post(client, email, password, route, json):
        headers = BaseApiTest._create_auth_header(client, email, password)
        return client.post(route, headers=headers, json=json)

    @staticmethod
    def auth_put(client, email, password, route, json):
        headers = BaseApiTest._create_auth_header(client, email, password)
        return client.put(route, headers=headers, json=json)

    @staticmethod
    def auth_delete(client, email, password, route):
        headers = BaseApiTest._create_auth_header(client, email, password)
        return client.delete(route, headers=headers)


if __name__ == '__main__':
    unittest.main()
