from urllib.parse import urljoin
from bs4 import BeautifulSoup

SECTIONS = [
    "post/adult-jobs",
    "post/bodyrubs",
    "post/dom-and-fetish",
    "post/escorts",
    "post/male-escorts",
    "post/ts",
    "post/phone-websites",
    "post/strippers-and-strip-clubs",
]


def twobackpage_com(html):
    soup = BeautifulSoup(html, "html.parser")
    ad_listing_urls = []
    geos = soup.find_all("div", class_="geoUnit")
    for geo in geos:
        for link in geo.find_all("a"):
            for section in SECTIONS:
                ad_listing_urls.append(urljoin(link.get("href"), section))
    return ad_listing_urls
