from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import (
    BaseAdListingParser,
    AdListing,
)


class OneBackPage_com(BaseAdListingParser):
    def ad_listings(self):
        ad_listings = []

        for post in self.soup.find_all("div", class_="thumbnail lister"):
            link = post.find("a", class_="list-title")
            url = link["href"]
            details = link.find_next_sibling("div", class_="locatio")
            city = details.find("span", class_="cityzen").text.strip()
            state = (details.find("span", class_="regionzen").text)[1:].strip()
            date = details.find("span", class_="utc_time")
            if (date is None):
                continue #skip adsense

            date = date.text.strip()

            ad_listings.append(
                AdListing(
                    url, metadata={"ad-date-posted": date,
                                   "location": city + ", " + state}
                )
            )

        return ad_listings

    def continuation_url(self):
        pagination_a = self.soup.find("a", class_="searchPaginationNext")
        if pagination_a:
            next_link = pagination_a["href"]
            parsed_url = urlparse(self.message["ad-listing-url"])
            if next_link:
                return urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", next_link)

    def ad_listing_data(self) -> dict:
        metadata = {}
        return metadata
