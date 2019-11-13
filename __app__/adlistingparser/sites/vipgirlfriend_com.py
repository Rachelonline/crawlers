from urllib.parse import urljoin
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import BaseAdListingParser


class VIPGirlfriend_com(BaseAdListingParser):
    def ad_listings(self):
        ad_listings = []

        listing_container = self.soup.find("div", class_="listing-simple")
        posts = listing_container.find_all("div", class_="card1")

        for post in posts:
          link = post.find("a")
          ad_listings.append(link.get("href"))

        return ad_listings

    def continuation_url(self):
        # There is no pagination; the "view more" button on this site
        # takes you to another region listing page
        return ""
