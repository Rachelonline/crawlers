from urllib.parse import urljoin, urlparse
import re
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import (
    BaseAdListingParser,
    AdListing,
)


class BackPage_ly(BaseAdListingParser):
    #AdListing(ad_url='https://new-york.bedpage.com/Bodyrubs/ues/9666285.html', metadata={'ad-date-posted': 'Thu 25 Jun', 'location': 'UES'}, custom_hash=None), AdListing(ad_url='https://new-york.bedpage.com/Bodyrubs/queens-blvd/9580546.html', metadata={'ad-date-posted': 'Thu 25 Jun', 'location': 'Queens Blvd '}, custom_hash=None)
    #Basically a comprehensive list of all the ad listings and their data in the format above.
    def ad_listings(self):
        ad_listings = []
        date = "Not found"
        for element in self.soup.findAll("li"):
            if element.get("class") == ['ad-date']:
                date = element.get_text()
            if element.get("class") == ['ad-list-item']:
                url = element.find("a", class_= "list-title").get("href")
                if "adserve" in url:
                    continue
                metadata = {}
                metadata["ad-date-posted"] = date
                metadata["location"] = element.find("small").get_text().replace('(', '').replace(')', '')
                ad_listings.append(AdListing(url, metadata = metadata))
        return ad_listings
    #https://new-york.bedpage.com/Bodyrubs/2 .https://new-york.bedpage.com/MenSeekMen/2
    #Finds the link to the next page of ad listings
    def continuation_url(self):
        url = self.soup.find("ul", class_= "pagination").find("a", class_="searchPaginationNext")
        if url == None:
            return
        return url.get("href")
    #{'location': 'New York, New York,   United States'} .{'location': 'Seattle, Washington,   United States'}
    #Finds the general data of that page of ad listings
    def ad_listing_data(self):
        metadata = {}
        metadata["location"] = self.soup.find("title").get_text().split("in ")[1].replace(' - BackPage(ly)', '')
        return metadata
