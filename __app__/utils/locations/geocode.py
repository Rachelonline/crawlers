from typing import List
import json
import os
import re
import requests
from __app__.utils.locations.redis_cache import cache_location

PATTERN = re.compile(r"[^\w ]+", re.UNICODE)
GOOGLE_GEO_API = "https://maps.googleapis.com/maps/api/geocode/json"
STOP_WORDS = {
    "outcall",
    "outcalls",
    "incall",
    "incalls",
    "only",
    "your",
    "bbbj",
    "asian",
    "girl",
    "sexy",
    "bbj",
    "suck",
    "2girls",
    "anal",
    "young",
    "korean",
    "years",
    "private",
}


@cache_location
def _geocode(location: str):
    params = {"key": os.environ["GOOGLE_MAPS_KEY"], "address": location, "limit": 1}
    resp = requests.get(GOOGLE_GEO_API, params=params)
    data = resp.json()
    if data["status"] == "OK":
        return data["results"][0]


def _clean_location(location: str) -> str:
    """
    Lowercases, remove puncutation and stop words
    """
    return " ".join(
        word
        for word in PATTERN.sub("", location.lower()).split()
        if word not in STOP_WORDS
    )


def _extract(component_name, location):
    return next((component for component in location["address_components"] if component_name in component["types"]), None)


def get_location(location: str) -> List:
    """
    Get the lat long of a location. Ignores stop words.
    """

    location = _geocode(_clean_location(location))
    if location:
        return {
            "country_code": _extract("country", location)["short_name"],
            "description": f'{_extract("locality", location)["long_name"]}, {_extract("administrative_area_level_1", location)["short_name"]}',
            "type": "Point",
            "coordinates": [
                location["geometry"]["location"]["lng"],
                location["geometry"]["location"]["lat"],
            ],
            "placeid": location["place_id"],
        }
