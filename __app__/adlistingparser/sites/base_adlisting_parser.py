from typing import List
from bs4 import BeautifulSoup
from typing import NamedTuple
from hashlib import sha1


class AdListing(NamedTuple):
    """
    This captures both the url and any metadata specific to that individual ad listing

    We need this because on certain sites (such as megapersonals.eu) the only place to get
    the date when the ad was posted is from the listing page, not on the ad itself.

    So we store that metadata in here and add it into the metadata in the ad-crawl message
    """

    ad_url: str
    metadata: dict = {}
    custom_hash: str = None

    def hash(self):
        """ hash to identify the unique ads"""
        ad_hash = sha1()
        hash_str = self.custom_hash or self.ad_url
        ad_hash.update(hash_str.encode())
        return ad_hash.hexdigest()


class BaseAdListingParser:
    def __init__(self, message):
        self.message = message
        self.soup = BeautifulSoup(message["ad-listing-page"], "html.parser")

    def ad_listings(self) -> List[AdListing]:
        """ returns a list of tuples, first the url and any metadata for the url"""
        raise NotImplementedError

    def continuation_url(self) -> str:
        """ returns the next url for depth crawling """
        raise NotImplementedError

    def ad_listing_data(self) -> dict:
        """ returns metadata for the ad listing page. Such as location, gender, etc """
        raise NotImplementedError
