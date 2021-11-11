"""Test File for the Artists Resource"""

from unittest import TestCase
from unittest.mock import Mock

from main import init_flask_api, init_flask_app


class ArtistResourceTest(TestCase):
    """Defines the test suite for the artists resources"""

    def setUp(self):
        self.app = init_flask_app()
        init_flask_api(self.app)
        self.client = self.app.test_client()

    def test_get_artists_no_params(self):
        """Tests the artists resource with no parameters"""
        response = self.client.get("/artists")
        body = response.get_json()

        if body is None:
            self.assertIsNotNone(body)
            raise Exception("Test request failed")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body["items"]), 20)

    def test_get_artists_limit(self):
        """Tests the artists resource with a limit parameter"""
        response = self.client.get("/artists?limit=10")
        body = response.get_json()

        if body is None:
            self.assertIsNotNone(body)
            raise Exception("Test request failed")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body["items"]), 10)

    def test_get_artists_fail(self):
        """Tests the artists resource with an incorrect parameter"""
        response = self.client.get("/artists?limit=ten")

        self.assertEqual(response.status_code, 500)

    def test_get_artists_extra_param(self):
        """Tests the artists resource with an extra param not in the model"""
        response = self.client.get("/artists?abc=123")

        self.assertEqual(response.status_code, 200)
