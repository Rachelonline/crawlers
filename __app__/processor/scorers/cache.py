import redis
import os


class RedisCache(object):
    def __init__(
        self, redis_host=os.environ.get("REDIS_HOST", "localhost"),
        password=os.environ.get("REDIS_KEY", None), port=os.environ.get("REDIS_PORT", 6379)
        ):
        self.redis = redis.Redis(
            host=redis_host, port=port, password=password
        )
        self.redis.ping()

    def get_cached_score(self, phone_number, score_key, default_score=None):
        """
        Return the cached score for a phone number and score key
        if it doesn't exist, then return the default_score argument
        """
        return self.redis.get(f"{phone_number}:{score_key}") or default_score
        

    def get_values_at_attribute(self, phone_number, score_type, attribute):
        _, keys = self.redis.scan(match=f"{phone_number}:{score_type}_{attribute}_*")
        data = self.redis.mget(keys)
        keys = [k.decode().split("_")[-1] for k in keys]
        return {k:d.decode() for k,d in zip(keys, data)}


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
    
    def increment_cached_score(self, phone_number, score_key, amount=1):
        """
        Increment the cached score by a certain amount and return
        the incremeneted score
        """
        # If the key doesnt exist and is incremented then there is no expiration
        return self.redis.incr(
            f"{phone_number}:{score_key}",
            amount
        )
