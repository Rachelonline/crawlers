from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import (
    BaseAdListingParser,
    AdListing,
)


class BackPage_ly(BaseAdListingParser):
    def ad_listings(self):
        ad_listings = []
        date = "Not found"
        for element in self.soup.findAll("li"):
            if element.get("class") == ['ad-date']:
                date = element.get_text()
            if element.get("class") == ['ad-list-item']:
                url = element.find("a", class_= "list-title").get("href")
                if "adserve" in url:
                    continue
                metadata = {}
                metadata["ad-date-posted"] = date
                metadata["location"] = element.find("small").get_text().replace('(', '').replace(')', '')
                ad_listings.append(AdListing(url, metadata = metadata))
        return ad_listings
    def continuation_url(self):
        url = self.soup.find("ul", class_= "pagination").find("a", class_="searchPaginationNext")
        if url == None:
            return
        return url.get("href")
    def ad_listing_data(self):
        metadata = {}
        metadata["location"] = self.soup.find("title").get_text().split("in ")[1].replace(' - BackPage(ly)', '')
        return metadata
