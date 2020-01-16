from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import BaseAdListingParser, AdListing


GENDER_MAPPING = {
    "Female Massage": "female",
    "Female Escorts": "female",
    "Female BDSM": "female",
    "Men": "male",
    "Male Escorts": "male",
    "Trans": "trans",
}

SERVICE_MAPPING = {"Female Massage": "massage", "Female BDSM": "bsdm"}


class EscortDirectory(BaseAdListingParser):
    DOMAIN = "https://www.escortdirectory.com"

    def ad_listings(self):
        ad_listings = []

        for ad_link in self.soup("a", class_="escort-item"):
            url = urljoin(self.DOMAIN, ad_link.get("href"))
            ad_listings.append(AdListing(url))
        return ad_listings

    def continuation_url(self):
        current = self.soup.find(class_="page-number grey active")
        if current:
            next_page = current.find_next_sibling("a")
            if next_page:
                return urljoin(self.DOMAIN, next_page["href"])

    def ad_listing_data(self) -> dict:
        metadata = {}

        # Find location
        location = self.soup.find(
            "div", class_="myCountry-mobile-place"
        )
        if location:
            metadata["location"] = " ".join(location.stripped_strings)

        # Gender can be from the listing!
        category = self.soup.find(
            "span", class_="lookingFor-mobile-place"
        )
        if category:
            category = " ".join(category.stripped_strings)
            gender = GENDER_MAPPING.get(category)
            if gender:
                metadata["gender"] = gender

            # Services
            service = SERVICE_MAPPING.get(category)
            if service:
                metadata["services"] = [service]
        return metadata
