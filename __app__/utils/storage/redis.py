import os
import redis

REDIS_HOST = "picrawling.redis.cache.windows.net"
REDIS = None


def get_connection():
    global REDIS
    if REDIS is None:
        REDIS = redis.Redis(
            host=REDIS_HOST, port=6380, db=0, password=os.environ["REDIS_KEY"], ssl=True
        )
    return REDIS
