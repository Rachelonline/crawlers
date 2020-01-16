import os
import json
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


def cache_location(function):
    def wrapper(*args, **kwargs):
        key = f"geo/{str(args)}/{str(kwargs)}"
        conn = get_connection()
        location = conn.get(key)
        if location is None:
            location = function(*args, **kwargs)
            if location is None:
                return
            location = json.dumps(location)
            conn.set(key, location)
        return json.loads(location)

    return wrapper
