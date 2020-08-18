from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import (
    BaseAdListingParser,
    AdListing,
)


class BedPage_com(BaseAdListingParser):
    def ad_listings(self):
        ad_listings = []

        for post in self.soup.select("div.cat > a:last-child"):
            url = post["href"]
            if "bedpage.com" not in url:
                continue #skip external urls

            metadata = {}
            metadata["ad-date-posted"] = post.parent.parent.select_one(".date").get_text()
            location_element = post.select_one("b")
            if location_element:
                metadata["location"] = location_element.get_text().split("( ")[-1][0:-1]

            ad_listings.append(AdListing(url, metadata=metadata))

        return ad_listings

    def continuation_url(self):
        return self.soup.find(text="Next").parent.get("href")

    def ad_listing_data(self) -> dict:
        metadata = {}

        # Find location
        metadata["location"] = ", ".join(reversed(self.soup.select_one("#cookieCrumb").get_text().split(" > ")[1:-1]))

        return metadata
