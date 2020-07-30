from urllib.parse import urljoin
from bs4 import BeautifulSoup


def capleasures_com(html):
    soup = BeautifulSoup(html, "html.parser")
    ad_listing_urls = []
    all_listings = soup.find("ul", class_="cities")
    for section in all_listings("li", recursive=False):
        for area in section("ul", class_="children", recursive=False):
            for region in area("li", recursive=False):
                ad_listing_link = region.find("a", recursive=False)
                ad_listing_urls.append(
                    urljoin("https://capleasures.com", ad_listing_link.get("href"))
                )
    return ad_listing_urls
