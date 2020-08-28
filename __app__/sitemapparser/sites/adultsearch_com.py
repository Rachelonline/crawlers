from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
import sys


# Catch regional subdomains.
def _find_domain(soup):
    uri = urlparse(
        soup.find("link", rel="canonical").get("href")
    )  # captures country subdomains

    return f"{uri.scheme}://{uri.netloc}"


# Attempt to return the soup of a tag's linked page.
def _get_linked_soup(tag, domain):
    resp = requests.get(urljoin(domain, tag.get("href")))

    if resp:
        return BeautifulSoup(resp.text, "html.parser")


# Each region page has several buttons for specific categories.
def get_category_soups(region_soups):
    category_soups = []
    for page in region_soups:
        sub_domain = _find_domain(page)
        category_buttons = page.select_one(".escort-services__buttons")

        for category_tag in category_buttons.select("a.btn-secondary-rounded"):
            category_count = category_tag.select_one(".btn-rounded-count")
            if category_count and category_count.text != "(0)":
                category_page = _get_linked_soup(category_tag, sub_domain)
                if category_page:
                    category_soups.append(category_page)

    return category_soups


# Sitemap has regional links by state and province for CA and US.
def get_region_soups(sitemap_soup):
    region_soups = []

    for region_tag in sitemap_soup.select("h5 > a"):
        region_page = _get_linked_soup(
            region_tag, ""
        )  # href of region tag includes subdomain
        if region_page:
            region_soups.append(region_page)

    return region_soups


# Retrieves ad listings from nested sitemap>region>category structure.
def adultsearch_com(html):
    sitemap_soup = BeautifulSoup(html, "html.parser")
    ad_listing_links = []

    region_soups = get_region_soups(sitemap_soup)
    category_soups = get_category_soups(region_soups)

    # Each category page links to city-specific ad listings.
    for page in category_soups:
        sub_domain = _find_domain(page)
        city_list = page.select_one(".city-list").select_one(".row")

        for city_tag in city_list.select("div > a"):
            full_listing_url = urljoin(sub_domain, city_tag.get("href"))
            ad_listing_links.append(full_listing_url)

    return ad_listing_links
