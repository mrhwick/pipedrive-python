from unittest import TestCase
from mock import patch
import responses
from pipedrive.Pipedrive import PipedriveAPIClient


class TestClientInitialization(TestCase):
    def test_api_token_as_string_creates_client(self):
        client = PipedriveAPIClient(api_token='some_api_token')
        self.assertIsNotNone(client);

    def test_api_token_as_string_persists_api_key(self):
        client = PipedriveAPIClient(api_token='some_api_token')
        self.assertEqual(client.api_token, "some_api_token")

    @patch("requests.post")
    def test_user_credentials_as_string_creates_client(self, requests_post_mock):
        client = PipedriveAPIClient(user_email="some_email@test.com", user_password="some_password")
        self.assertIsNotNone(client)

    @patch("requests.post")
    def test_user_credentials_as_string_calls_requests(self, requests_post_mock):
        PipedriveAPIClient(user_email="some_email@test.com", user_password="some_password")
        self.assertTrue(requests_post_mock.called)

    @responses.activate
    def test_user_credentials_as_string_persists_api_token(self):
        responses.add(
            responses.POST,
            "https://api.pipedrive.com/v1/authorizations",
            body='{"success": true, "data": [{"api_token": "some_unique_api_token"}]}',
            status=200,
            content_type='application/json',
        )
        client = PipedriveAPIClient(user_email="some_email@test.com", user_password="some_password")
        self.assertEqual(client.api_token, "some_unique_api_token")

    def test_api_token_not_as_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            PipedriveAPIClient(api_token=1234)

        with self.assertRaises(ValueError):
            PipedriveAPIClient(api_token=object)

        with self.assertRaises(ValueError):
            PipedriveAPIClient(api_token=object())

    def test_user_credentials_not_as_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            PipedriveAPIClient(user_email=1234, user_password="some_pass")

        with self.assertRaises(ValueError):
            PipedriveAPIClient(user_email="some_email@test.com", user_password=5678)

        with self.assertRaises(ValueError):
            PipedriveAPIClient(user_email=1234, user_password=5678)

        with self.assertRaises(ValueError):
            PipedriveAPIClient(user_email=object(), user_password="some_pass")

        with self.assertRaises(ValueError):
            PipedriveAPIClient(user_email="some_email@test.com", user_password=object())

        with self.assertRaises(ValueError):
            PipedriveAPIClient(user_email=object(), user_password=object())
