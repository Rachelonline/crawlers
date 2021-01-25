from typing import List
import re
import geocoder
from __app__.utils.locations.redis_cache import cache_location

PATTERN = re.compile(r"[^\w ]+", re.UNICODE)
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
    geocoded_location = geocoder.osm(location, maxRows=1)
    if geocoded_location.ok:
        return geocoded_location


def _clean_location(location: str) -> str:
    """
    Lowercases, remove punctuation and stop words
    """
    return " ".join(
        word
        for word in PATTERN.sub("", location.lower()).split()
        if word not in STOP_WORDS
    )


def get_location(location: str) -> List:
    """
    Get the lat long of a location. Ignores stop words.
    """

    location = _geocode(_clean_location(location))
    if location:
        return {
            "country_code": location.country_code.upper(),
            "description": location.address,
            "type": "Point",
            "coordinates": [
                location.lng,
                location.lat,
            ],
            "osm_id": location.osm_id,
        }
