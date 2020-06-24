from urllib.parse import urljoin
from bs4 import BeautifulSoup


def usaadultclassified_nl(html):
    # Just a top-level website
    # Going forward, we can probably look at
    # passing a metadata parameter alongside
    # the html payload itself
    return ["http://usaadultclassified.nl/c/united-states"]
