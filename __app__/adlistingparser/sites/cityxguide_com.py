from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import BaseAdListingParser, AdListing

PAGE_NUM_RE = re.compile(r"(.*cityxguide.com.*/page/)([0-9]+)/?$")

# We dont wan't to include these in the extracted location string
REMOVE_FROM_LOCATATION_STR = set(
    [
        "HOME",
        "Africa",
        "Asia, Pacific & Middle East",
        "Australia & Oceania",
        "Europe",
        "Latin America & Caribbean",
    ]
)


class CityXGuide_com(BaseAdListingParser):
    def ad_listings(self):
        ad_listings = []

        # Note: Sponsored Ads are loaded in with javascript - we don't capture them
        for post in self.soup("ul", class_="postlist"):
            for ad_link in post("a"):
                url = urljoin("https://cityxguide.com/", ad_link.get("href"))
                ad_listings.append(AdListing(url))
        return ad_listings

    def continuation_url(self):
        # The next button is loaded with javascript, but we know it's the next number in the url
        current_url = self.message["ad-listing-url"]
        new_url = PAGE_NUM_RE.sub(
            lambda x: f"{x.group(1)}{str(int(x.group(2)) + 1)}/", current_url
        )
        if new_url != current_url:
            return new_url
        return f"{current_url}/page/2/"

    def ad_listing_data(self) -> dict:
        metadata = {}

        # Find location
        locations = []
        breadcrumb = self.soup.find("div", class_="breadcrumbs")
        for span in breadcrumb.find_all("span", {"itemprop": "name"}):
            span_text = span.text
            if span_text not in REMOVE_FROM_LOCATATION_STR:
                locations.append(span_text)
        if locations:
            metadata["location"] = ", ".join(locations)

        # CityXGuide is mostly all females, we check ad itself for others
        metadata["gender"] = "female"
        return metadata
