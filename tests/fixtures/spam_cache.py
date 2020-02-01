import pytest
from collections import defaultdict
from unittest.mock import MagicMock, patch, PropertyMock


class TestCache(object):
    def __init__(self):
        self.test_cache = {}
        self.test_hcache = defaultdict(dict)

    def get_cached_score(self, phone_number, score_key, default_score=None):
        return self.test_cache.get(f"{phone_number}:{score_key}", default_score)

    def put_cached_score(self, phone_number, score_key, score, expire=False):
        self.test_cache[f"{phone_number}:{score_key}"] = score
        return score

    def get_values_at_attribute(self, phone_number, score_type, attribute):
        return {}

    def put_cached_list(self, phone_number, score_key, value_list):
        self.test_hcache[phone_number][score_key] = value_list

    def get_hset_values(self, phone_number, attribute):
        return {}

    def add_to_cached_list(self, phone_number, score_key, value):
        _current_list = self.test_hcache.get(phone_number, {}).get(score_key, None)
        if _current_list:
            _current_list.append(value)
        else:
            _current_list = [value]

        self.put_cached_list(phone_number, score_key, _current_list)
        return _current_list

    def increment_cached_score(self, phone_number, score_key, amount=1):
        """
        Increment the cached score by a certain amount and return
        the incremeneted score
        """
        # If the key doesnt exist and is incremented then there is no expiration
        current_score = self.test_cache.get(f"{phone_number}:{score_key}", 0)
        self.test_cache[f"{phone_number}:{score_key}"] = current_score + amount
        return self.get_cached_score(phone_number, score_key)


@pytest.fixture(autouse=True)
def test_cache():
    return TestCache()
