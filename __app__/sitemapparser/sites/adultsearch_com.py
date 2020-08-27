from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests


# Catch regional subdomains.
def _find_domain(soup):
    uri = urlparse(
        soup.find("link", rel="canonical").get("href")
    )  # captures country subdomains

    print("sub domain will be " + f"{uri.scheme}://{uri.netloc}")
    return f"{uri.scheme}://{uri.netloc}"


# Attempt to return the soup of a tag's linked page.
def _get_soup_from_tag(tag, domain="https://www.adultsearch.com"):
    link = tag.get("href")
    resp = requests.get(urljoin(domain, link))

    if resp:
        return BeautifulSoup(resp.text)


# Each region page has several buttons for specific categories.
def get_category_soups(region_soups):
    category_soups = []
    for page in region_soups:
        sub_domain = _find_domain(page)

        for category_tag in page.select("a .btn-secondary-rounded"):
            category_count = category_tag.select_one(".btn-rounded.count")
            if category_count.text != "(0)":
                city_page = _get_soup_from_tag(category_tag, sub_domain)
                if city_page:
                    category_soups.append(city_page)

    return category_soups


# Sitemap has regional links by state and province for CA and US.
def get_region_soups(sitemap_soup):
    region_soups = []

    for region_tag in sitemap_soup.select("h5 > a"):
        category_page = _get_soup_from_tag(region_tag)
        if category_page:
            region_soups.append(category_page)

    return region_soups


# Retrieve ad listings from nested sitemap>region>category structure.
def _get_ad_listing_links(sitemap_soup):
    ad_listing_links = []

    region_soups = get_region_soups(sitemap_soup)
    category_soups = get_category_soups(region_soups)

    # Each category page links to the city-specific ad listings.
    for page in category_soups:
        sub_domain = _find_domain(page)

        for city_tag in page.select("div > a"):
            full_listing_url = urljoin(sub_domain, city_tag.get("href"))
            print("full listing url would be " + full_listing_url)
            ad_listing_links.append(full_listing_url)

    return ad_listing_links


def adultsearch_com(html):
    soup = BeautifulSoup(html, "html.parser")
    ad_listing_urls = []

    for link in _get_ad_listing_links(soup):
        ad_listing_urls.append(link)

    return ad_listing_urls
