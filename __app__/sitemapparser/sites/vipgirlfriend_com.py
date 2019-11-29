from urllib.parse import urljoin
from bs4 import BeautifulSoup


def vipgirlfriend_com(html):
    soup = BeautifulSoup(html, "html.parser")
    ad_listings_urls = []
    top_level_menu = soup.find("ul", id="menu-main")
    for link in top_level_menu("a"):
        ad_listings_urls.append(link.get("href"))
    return ad_listings_urls
