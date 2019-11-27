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

    def ad_listing_data(self) -> dict:
        metadata = {}

        # Find location
        location = self.soup.find(
            "div", class_="myCountry-mobile-place"
        ).stripped_strings
        metadata["location"] = " ".join(location)

        # Gender can be from the listing!
        gender = self.soup.find(
            "span", class_="lookingFor-mobile-place"
        ).stripped_strings
        gender = " ".join(gender).lower()
        gender = gender.replace(" escorts", "")
        # TODO: Do this better
        if gender == "men":
            gender = "male"
        metadata["gender"] = gender
        return metadata
