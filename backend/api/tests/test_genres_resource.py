"""Test File for the Genres Resource"""

import operator
from unittest import TestCase

from main import init_flask_api, init_flask_app
from pytest import raises as pytest_raises
from resources.genres import Genres, filter_dict


class GenresResourceTest(TestCase):
    """Defines the test suite for the genres resources"""

    def setUp(self):
        self.app = init_flask_app()
        init_flask_api(self.app)
        self.client = self.app.test_client()
        self.genres = Genres()
        self.genres.genre_detail = {
            "hip hop": 1,
            "experimental hip hop": 6,
            "alt rock": 10,
            "indie rock": 8,
            "pop": 5,
        }

    def test_get_genres_no_params(self):
        """Tests the genres resource with no parameters"""
        response = self.client.get("/genres")
        body = response.get_json()

        if body is None:
            self.assertIsNotNone(body)
            raise Exception("Test request failed")

        self.assertEqual(response.status_code, 200)

    def test_get_genres_limit(self):
        """Tests the genres resource with a limit parameter"""
        response = self.client.get("/genres?limit=10")
        body = response.get_json()

        if body is None:
            self.assertIsNotNone(body)
            raise Exception("Test request failed")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body["items"]), 10)

    def test_get_genres_invalid_param(self):
        """Tests the genres resource with an incorrect parameter"""
        response = self.client.get("/genres?limit=ten")

        self.assertEqual(response.status_code, 500)

    def test_get_genres_extra_param(self):
        """Tests the genres resource with an extra param not in the model"""
        response = self.client.get("/genres?abc=123")

        self.assertEqual(response.status_code, 200)

    def test_sort_genres_by_count(self):
        """Tests that the sort genres method returns a dict sorted by value"""
        sorted_genres = self.genres._Genres__sort_genres_by_count()  # type: ignore
        self.assertDictEqual(
            sorted_genres,
            {
                "alt rock": 10,
                "indie rock": 8,
                "experimental hip hop": 6,
                "pop": 5,
                "hip hop": 1,
            },
        )

    def test_aggregate_genres(self):
        """Tests that detailed genres are aggregated into larger bins"""
        with self.app.app_context():
            self.genres._Genres__aggregate_genres()  # type: ignore

        self.assertDictEqual(
            self.genres.genre_aggregate,
            {
                "rock": 18,
                "hip hop": 7,
                "pop": 5,
                "rap": 0,
                "r&b": 0,
                "metal": 0,
                "indie": 8,
                "soul": 0,
                "folk": 0,
                "electronic": 0,
                "country": 0,
            },
        )

    def test_filter_dict_success(self):
        """Tests that filter dict works with the corrent args"""
        filtered = filter_dict({"in": 1, "out": 0, "in&out": 2}, operator.contains, "u")
        self.assertEqual(filtered, [0, 2])

    def test_filter_dict_failure(self):
        """Tests that filter dict raises as type error when it is called with an
        operator function and query value that are incompatible with the str type
        """
        with pytest_raises(TypeError):
            filter_dict({"in": 1, "out": 0}, operator.floordiv, 3)
