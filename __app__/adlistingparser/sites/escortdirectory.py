from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import BaseAdListingParser

class EscortDirectory(BaseAdListingParser):
    DOMAIN = "https://www.escortdirectory.com"

    def ad_listings(self):
        ad_listings = []

        for ad_link in self.soup("a", class_="escort-item"):
            url = urljoin(self.DOMAIN, ad_link.get("href"))
            ad_listings.append(url)
        return ad_listings

    def continuation_url(self):
        current = self.soup.find(class_="page-number grey active")
        next_page = current.find_next_sibling("a")
        if next_page:
            return urljoin(self.DOMAIN, next_page["href"])
