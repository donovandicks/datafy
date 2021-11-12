"""Test File for the Songs Resource"""

from unittest import TestCase

from main import init_flask_api, init_flask_app


class SongsResourceTest(TestCase):
    """Defines the test suite for the songs resources"""

    def setUp(self):
        self.app = init_flask_app()
        init_flask_api(self.app)
        self.client = self.app.test_client()

    def test_get_songs_no_params(self):
        """Tests the songs resource with no parameters"""
        response = self.client.get("/songs")
        body = response.get_json()

        if body is None:
            self.assertIsNotNone(body)
            raise Exception("Test request failed")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body["items"]), 20)

    def test_get_songs_limit(self):
        """Tests the songs resource with a limit parameter"""
        response = self.client.get("/songs?limit=10")
        body = response.get_json()

        if body is None:
            self.assertIsNotNone(body)
            raise Exception("Test request failed")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body["items"]), 10)

    def test_get_songs_invalid_param(self):
        """Tests the songs resource with an incorrect parameter"""
        response = self.client.get("/songs?limit=ten")

        self.assertEqual(response.status_code, 500)

    def test_get_songs_extra_param(self):
        """Tests the songs resource with an extra param not in the model"""
        response = self.client.get("/songs?abc=123")

        self.assertEqual(response.status_code, 200)
