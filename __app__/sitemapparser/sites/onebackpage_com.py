from urllib.parse import urljoin
from bs4 import BeautifulSoup

SELECTORS = ["sRegion", "sCity"]
BASE_URL = "https://onebackpage.com/index.php?page=search&sPattern=&"


def onebackpage_com(html):
    soup = BeautifulSoup(html, "html.parser")
    ad_listing_urls = []

    for selector in SELECTORS:
        sSelector = soup.find_all("select", {"name": selector})
        for srange in sSelector:
            for option in srange.find_all("option"):
                if option["value"]:
                    ad_listing_urls.append(
                        urljoin(BASE_URL, f"{selector}={option['value']}")
                    )

    return ad_listing_urls
