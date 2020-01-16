import pytest
from unittest.mock import MagicMock, patch, PropertyMock


class TestCache(object):
    def __init__(self):
        self.test_cache = {}

    def get_cached_score(
        self, phone_number, score_key, default_score=None
    ):
        return self.test_cache.get(
            f"{phone_number}:{score_key}", default_score
        )

    def put_cached_score(
        self, phone_number, score_key, score, expire=False
    ):
        self.test_cache[
            f"{phone_number}:{score_key}"
        ] = score
        return score

    def get_values_at_attribute(self, phone_number, score_type, attribute):
        return {}


    def increment_cached_score(
        self, phone_number, score_key, amount=1
    ):
        """
        Increment the cached score by a certain amount and return
        the incremeneted score
        """
        # If the key doesnt exist and is incremented then there is no expiration
        current_score = self.test_cache.get(
            f"{phone_number}:{score_key}", 0
        )
        self.test_cache[f"{phone_number}:{score_key}"] = (
            current_score + amount
        )
        return self.get_cached_score(
            phone_number, score_key
        )


@pytest.fixture(autouse=True)
def test_cache():
    return TestCache()
