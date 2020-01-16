from urllib.parse import urljoin
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import BaseAdListingParser, AdListing


IGNORE_LOCATIONS = set(["Home"])


class VIPGirlfriend_com(BaseAdListingParser):
    def ad_listings(self):
        ad_listings = []

        listing_container = self.soup.find("div", class_="listing-simple")
        posts = listing_container.find_all("div", class_="card1")

        for post in posts:
            link = post.find("a")
            ad_listings.append(AdListing(link.get("href")))

        return ad_listings

    def continuation_url(self):
        # There is no pagination; the "view more" button on this site
        # takes you to another region listing page
        return ""

    def ad_listing_data(self) -> dict:
        metadata = {}

        # Find location
        locations = []
        breadcrumb = self.soup.find("div", class_="page-heading")
        for ul in breadcrumb.find_all("ul", class_="breadcrumbs"):
            ul_text = ul.text
            ul_text = ul_text.replace("Home Escorts »", "")
            ul_text = ul_text.replace("Escorts", "")
            ul_text = ul_text.replace("Home", "")
            ul_text = ul_text.strip()
            if ul_text not in IGNORE_LOCATIONS:
                locations.append(ul_text)
        if locations:
            metadata["location"] = ", ".join(locations)

        metadata["gender"] = "female"
        return metadata
