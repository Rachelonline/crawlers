from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

_domain = "https://www.adultsearch.com"
# <link rel="canonical" href="https://ca.adultsearch.com/alberta/calgary"/>

# Attempt to return the soup of a tag's linked page.
def _get_soup_from_tag(tag):
    link = tag.get("href")
    resp = requests.get(urljoin(_domain, link))

    if resp:
        return BeautifulSoup(resp.text)


# Sitemap has regional links by state and province for CA and US.
def _get_region_soups(sitemap_soup):
    region_soups = []

    for region_tag in sitemap_soup.select("h5 > a"):
        category_page = _get_soup_from_tag(region_tag)
        if category_page:
            region_soups.append(category_page)

    return region_soups


# Each region page has several buttons for specific categories.
def _get_category_soups(region_soups):
    category_soups = []
    for page in region_soups:
        for category_tag in page.select("a .btn-secondary-rounded"):
            category_count = category_tag.select_one(".btn-rounded.count")
            if category_count.text is not "(0)":
                city_page = _get_soup_from_tag(category_tag)
                if city_page:
                    category_soups.append(city_page)

    return category_soups


def _get_ad_listing_links(sitemap_soup):
    ad_listing_links = []

    region_soups = _get_region_soups(sitemap_soup)
    category_soups = _get_category_soups(region_soups)

    # Each category page links to the city-specific ad listings.
    for page in category_soups:
        for city_tag in page.select("div > a"):
            ad_listing_links.append(city_tag.get("href"))

    return ad_listing_links


def adultsearch_com(html):
    soup = BeautifulSoup(html, "html.parser")
    ad_listing_urls = []

    for link in _get_ad_listing_links(soup):
        ad_listing_urls.append(urljoin(_domain, link))

    return ad_listing_urls
