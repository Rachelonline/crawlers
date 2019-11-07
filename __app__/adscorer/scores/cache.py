import os
from urllib.parse import urlparse
import redis

REDIS_HOST = "picrawling.redis.cache.windows.net"

class RedisCache(object):
    def __init__(self, redis_host=REDIS_HOST, password=os.environ["REDIS_KEY"]):
        self.redis = redis.Redis(
            host=redis_host, port=6380, db=0, password=password, ssl=True
        )
        self.redis.ping()

    def get_cached_score(self, phone_number, score_key):
        """
        Return the cached score for a phone number and score key
        """
        return self.redis.mget(f"{phone_number}:{score_key}")
        

    def put_cached_score(self, phone_number, score_key, score, expire=False):
        """
        Put an updated cached score for a phone number and score key
        """
        return self.redis.set(
            f"{phone_number}:{score_key}",
            score,
            nx=False, # Always set the value
            ex=expire
        )
