from typing import List
from bs4 import BeautifulSoup


class BaseAdListingParser:
    def __init__(self, message):
        self.message = message
        self.soup = BeautifulSoup(message["ad-listing-page"], "html.parser")

    def ad_listings(self) -> List[str]:
        """ returns a list of tuples, first the url and any metadata for the url"""
        raise NotImplementedError

    def continuation_url(self) -> str:
        """ returns the next url for depth crawling """
        raise NotImplementedError
