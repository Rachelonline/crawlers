from typing import List
from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import (
    BaseAdListingParser,
    AdListing,
)


class USAAdultClassified(BaseAdListingParser):

    def ad_listings(self) -> List[AdListing]:
        ad_listings = []
        posts = self.soup.select('tr.post1')

        for p in posts:
            url = f"https://usaadultclassified.nl{p.find('a', class_='posttitle')['href']}"

            try:
                div = p.select('div')[1]
                ad_name = div.find('b')
                if ad_name is not None:
                    ad_name = ad_name.text

                ad_title = div.text

                ad_location = p.select('font')[0].text

                metadata = {
                    "ad-name": ad_name,
                    "ad_title": ad_title,
                    "ad_location": ad_location
                }

            except Exception:
                metadata = {}

            ad_listings.append(AdListing(url, metadata=metadata))

        return ad_listings

    def continuation_url(self) -> str:
        return self.soup.select('.page-link.next')['href']

    def ad_listing_data(self) -> dict:
        return {}
