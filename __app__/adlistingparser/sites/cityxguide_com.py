from urllib.parse import urljoin
from bs4 import BeautifulSoup


def _ad_listings(soup):
    ad_listings = []

    # Note: Sponsored Ads are loaded in with javascript - we don't capture them
    for post in soup("ul", class_="postlist"):
        for ad_link in post("a"):
            ad_listings.append(urljoin("https://cityxguide.com/", ad_link.get("href")))
    return ad_listings


def _next_urls(soup):
    next_urls = []
    return next_urls


def cityxguide_com(html):
    soup = BeautifulSoup(html, "html.parser")
    ad_listing_urls = _ad_listings(soup)
    next_urls = _next_urls(soup)
    return ad_listing_urls, next_urls
