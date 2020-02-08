from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import (
    BaseAdListingParser,
    AdListing,
)


class GfeMonkey_com(BaseAdListingParser):
    def ad_listings(self):
        ad_listings = []
        for post in self.soup.find_all("div", class_="card"):
            for ad_link in post("a", recursive=False):
                url = urljoin("https://www.gfemonkey.com", ad_link.get("href"))
                ad_listings.append(AdListing(url))
        return ad_listings

    def continuation_url(self):
        next_link = self.soup.find("a", class_="next")
        if next_link:
            return urljoin("https://www.gfemonkey.com", next_link.get("href"))

        see_more_link = self.soup.find("a", class_="see-more")
        if see_more_link:
            return urljoin("https://www.gfemonkey.com", see_more_link.get("href"))

    def ad_listing_data(self) -> dict:
        metadata = {}

        # Find location
        breadcrumb = self.soup.find("div", class_="breadcrumbs-container")
        if breadcrumb:
            span = breadcrumb.find("span", class_="long")
            span_text = span.text
            if span_text:
                metadata["location"] = span_text

        # GFE is all females, we check ad itself for others
        metadata["gender"] = "female"
        return metadata
