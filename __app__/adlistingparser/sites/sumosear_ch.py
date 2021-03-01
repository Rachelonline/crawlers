from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import (
    BaseAdListingParser,
    AdListing,
)


class SumoSear_ch(BaseAdListingParser):
    def ad_listings(self):
        ad_listings = []
        for item in self.soup.findAll("a", class_="img-res-item"):
                url = item.get("href")
                metadata = {}
                time = item.find("time", class_="img-res-item__time").get_text()
                if time:
                    metadata["ad-date-posted"] = time
                ad_listings.append(AdListing(url, metadata = metadata))
        return ad_listings

    def continuation_url(self):
        url = self.soup.find("a", class_="pagination__link nav-arrow")
        if url:
            return url.get("href")

    def ad_listing_data(self):
        metadata = {}
        data = self.soup.findAll("span", class_="tags-row__item-name")
        category = data[1].get_text()
        if "Female" in category:
            metadata["gender"] = "female"
        elif "Male" in category:
            metadata["gender"] = "male"
        elif "Trans" in category:
            metadata["gender"] = "transgender"
        return metadata
