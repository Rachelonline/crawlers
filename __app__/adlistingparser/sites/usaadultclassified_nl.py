from urllib.parse import urljoin
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import BaseAdListingParser, AdListing


def usaadultclassified_nl(html):
    # TODO: this is actually for adparser
    soup = BeautifulSoup(html, "html.parser")
    return [x['href'] for x in soup.find_all("a", class_="posttitle")]