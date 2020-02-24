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

        for post in self.soup.find_all("a", class_="list-title"):
            for ad_link in post("a"):
                url = ad_link["href"]
                details = post.find_next_sibling("div", class_="locatio")
                location = details.find_all("span", class_="regionzen hidden-ari-down")[
                    0
                ].text
                date = details.find_all("span", class_="utc_time")[0].text
                ad_listings.append(
                    AdListing(
                        url, metadata={"ad-date-posted": date, "location": location}
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
