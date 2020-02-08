import redis
import json
import os
from __app__.utils.storage.redis import get_connection


class RedisCache(object):
    def __init__(self):
        self.redis = get_connection()
        self.redis.ping()

    def get_cached_score(self, phone_number, score_key, default_score=None):
        """
        Return the cached score for a phone number and score key
        if it doesn't exist, then return the default_score argument
        """
        return self.redis.get(f"{phone_number}:{score_key}") or default_score

    def get_hset_values(self, phone_number, attribute):
        # TODO: refactor this
        pairs = self.redis.hscan_iter(phone_number, attribute)
        for result in pairs:
            keys = result[0].decode()
            data = result[0].decode()
            keys = [k.decode().split("_")[-1] for k in keys]
            return {k: d for k, d in zip(keys, data)}
        return {}

    def get_values_at_attribute(self, phone_number, score_type, attribute):
        _, keys = self.redis.scan(match=f"{phone_number}:{score_type}_{attribute}_*")
        data = self.redis.mget(keys)
        keys = [k.decode().split("_")[-1] for k in keys]
        return {k: d.decode() for k, d in zip(keys, data)}

    def put_cached_score(self, phone_number, score_key, score, expire=False):
        """
        Put an updated cached score for a phone number and score key
        """
        return self.redis.set(
            f"{phone_number}:{score_key}",
            score,
            nx=False,  # Always set the value
            ex=expire,
        )

    def put_cached_list(self, phone_number, score_key, value_list):
        return self.redis.hset(phone_number, score_key, value_list)

    def read_cached_list(self, phone_number, score_key):
        """
        """
        return self.redis.hget(phone_number, score_key)

    def add_to_cached_list(self, phone_number, score_key, value):
        """
        Increment the cached score by a certain amount and return
        the incremeneted score
        """
        _current_list = self.read_cached_list(phone_number, score_key)
        if _current_list:
            # If there is a list already there, append to it
            _current_list = json.loads(_current_list)
            _current_list.append(value)
        else:
            # Otherwise, create a new one with the current value
            _current_list = [value]

        self.put_cached_list(phone_number, score_key, json.dumps(_current_list))

        return _current_list

    def increment_cached_score(self, phone_number, score_key, amount=1):
        """
        Increment the cached score by a certain amount and return
        the incremeneted score
        """
        # If the key doesnt exist and is incremented then there is no expiration
        return self.redis.incr(f"{phone_number}:{score_key}", amount)
