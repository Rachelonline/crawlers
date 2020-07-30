from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://onebackpage.com/"
ORDER_PARAMS = "/sOrder,dt_pub_date/iOrderType,desc"


def onebackpage_com(html):
    soup = BeautifulSoup(html, "html.parser")
    ad_listing_urls = []

    states = soup.find("select", {"name": "sRegion"})
    for option in states.find_all("option"):
        if option["value"]:
            ad_listing_urls.append(
                urljoin(BASE_URL, f"search/region,{option['value']}{ORDER_PARAMS}")
            )

    return ad_listing_urls
