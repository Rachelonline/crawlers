import redis

REDIS_HOST = "picrawling.redis.cache.windows.net"

class RedisCache(object):
    def __init__(self, redis_host=REDIS_HOST, password=os.environ["REDIS_KEY"]):
        self.redis = redis.Redis(
            host=redis_host, port=6380, db=0, password=password, ssl=True
        )
        self.redis.ping()

    def get_cached_score(self, phone_number, score_key, default_score=None):
        """
        Return the cached score for a phone number and score key
        if it doesn't exist, then return the default_score argument
        """
        return self.redis.get(f"{phone_number}:{score_key}") or default_score
        

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
