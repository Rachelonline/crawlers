from typing import List
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import json

URL_PREFIX = "https://megapersonals.eu/public/post_list"
# Each one of these represents different categories:
#  1 - Female (straight)
#  2 - Male (straight)
#  3 - Male (gay)
#  4 - Female (gay)
#  5 - Trans
CATEGORIES = [1, 2, 3, 4, 5]


def extract_listing_data(script) -> dict:
    """
    Extracts the location element in the script tag, if it exists
    """
    text = script.string
    if text is None:
        return
    script_splits = text.split("var data = JSON.parse(", maxsplit=1)
    if len(script_splits) > 1:
        data = script_splits[1].strip().split("' ||")[0]
        return json.loads(data[1:])


def convert_listings_to_urls(data: dict) -> List[str]:
    """
    Converts the data in the script tag into the ad listing urls.
    """
    ad_listing_urls = []
    for continent in data.values():
        for state in continent["states"].values():
            for city in state["cities"]:
                for category in CATEGORIES:
                    ad_listing_url = f"{URL_PREFIX}/{city['id']}/{category}/1"
                    ad_listing_urls.append(ad_listing_url)
    return ad_listing_urls


def megapersonals_eu(html):
    soup = BeautifulSoup(html, "html.parser")
    ad_listing_urls = []

    scripts = soup.find_all("script")
    for script in scripts:
        data = extract_listing_data(script)
        if data:
            ad_listing_urls = convert_listings_to_urls(data)
    return ad_listing_urls
