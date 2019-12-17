from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import (
    BaseAdListingParser,
    AdListing,
)

# We dont wan't to include these in the extracted location string
REMOVE_FROM_LOCATATION_STR = set(
    [
        "Home",
        "Africa",
        "Asia, Pacific, and Middle East",
        "Australia and Oceania",
        "Europe",
        "Latin America and Caribbean",
        " >",
        "Adult Jobs",
        "Bodyrubs",
        "Dom and Fetish",
        "Male Escorts",
        "TS",
        "Phone & Websites",
        "Strippers and strip Clubs",
        "Escorts",
        "Male",
    ]
)

GENDER_MAPPING = {"Male": "male", "TS": "trans"}

SERVICES_MAPPING = {
    "Adult Jobs": "adult jobs",
    "Bodyrubs": "Bodyrubs",
    "Dom and Fetish": "dom and fetish",
    "Escorts": "escorts",
    "Male Escorts": "escorts",
    "TS": "escorts",
    "Phone & Websites": "phone & websites",
    "Strippers and strip Clubs": "strippers and strip clubs",
}


class TwoBackpage_com(BaseAdListingParser):
    def ad_listings(self):
        ad_listings = []

        # Normal listings + top sponsored
        #  Note: We don't capture the side sponsored panel yet
        for post in self.soup.find_all("div", class_="cat"):
            for ad_link in post("a"):
                url = ad_link["href"]
                prev_date = post.find_previous_sibling("div", class_="date")
                if prev_date:
                    prev_date = prev_date.text.strip()
                    ad_listings.append(
                        AdListing(url, metadata={"ad-date-posted": prev_date})
                    )
                else:
                    ad_listings.append(AdListing(url))

        return ad_listings

    def continuation_url(self):
        pagination_div = self.soup.find("div", class_="pagination")
        if pagination_div:
            next_link = pagination_div.find("a", {"rel": "next"})
            parsed_url = urlparse(self.message["ad-listing-url"])
            if next_link:
                return urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", next_link["href"])

    def ad_listing_data(self) -> dict:
        metadata = {}

        # Find location
        breadcrumb = self.soup.find("div", id="cookieCrumb")
        if breadcrumb:
            location = " ".join(breadcrumb.stripped_strings)

            # Gender
            for k, v in GENDER_MAPPING.items():
                if k in location:
                    metadata["gender"] = v
                    break
            if "gender" not in metadata:
                metadata["gender"] = "female"

            # Service
            for k, v in SERVICES_MAPPING.items():
                if k in location:
                    metadata["services"] = [v]
                    break

            # Location
            for remove in REMOVE_FROM_LOCATATION_STR:
                location = location.replace(remove, "")
            if location:
                metadata["location"] = location.strip()

        return metadata
