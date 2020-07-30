from urllib.parse import urljoin
from bs4 import BeautifulSoup


def gfemonkey_com(html):
    soup = BeautifulSoup(html, "html.parser")
    ad_listings_urls = []
    top_level_menu = soup.find("nav", class_="sliding-menu-content")
    for link in top_level_menu.find_all("a"):
        if link.get("href") == "/":
            # don't use home link
            continue
        ad_listings_urls.append(link.get("href") + "/all-escorts")
    return [f"https://www.gfemonkey.com{ad_url}" for ad_url in ad_listings_urls]
