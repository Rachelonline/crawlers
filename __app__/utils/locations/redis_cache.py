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
    """
    Caches the geocoding under a set of 2 keys. The location is mapped to a placeid
    then the placeid has it's data
    conceptually: "seattle wa" -> "ZJHsd34" and "ZJHsd34" -> {geo data}

    This allows us to look up geo information later with just the place id (which is saved
    with the ad)
    """

    def wrapper(*args, **kwargs):
        key = f"geo/{str(args)}/{str(kwargs)}"
        conn = get_connection()
        place_id = conn.get(key)
        if place_id is None:
            place_id = ""
        location = conn.get(place_id)
        if location is None:
            location = function(*args, **kwargs)
            if location is None:
                return
            place_id = location["place_id"]
            location = json.dumps(location)
            conn.set(key, place_id)
            # Not worried about the race condition, data is the same for both
            if not conn.exists(place_id):
                conn.set(place_id, location)
        return json.loads(location)

    return wrapper


def get_place(place_id: str) -> dict:
    """
    Gets the geo data for a place from our cache
    """
    if not place_id:
        return
    conn = get_connection()
    data = conn.get(place_id)
    if data:
        return json.loads(data)
