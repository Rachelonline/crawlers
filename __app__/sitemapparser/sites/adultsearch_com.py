from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
import sys

# Each region page has several buttons for specific categories.
def get_category_pages(region_pages):
    category_pages = []
    for page in region_pages:
        sub_domain = _find_domain(page)
        category_buttons = page.select_one(".escort-services__buttons")

        for button in category_buttons.select("a.btn-secondary-rounded"):
            category_count = button.select_one(".btn-rounded-count")
            if category_count and category_count.text != "(0)":
                page = _get_linked_page(button, sub_domain)
                if page:
                    category_pages.append(page)

    return category_pages


# Sitemap has regional links by state and province for CA and US.
def get_region_pages(sitemap_soup):
    region_pages = []

    for region_tag in sitemap_soup.select("h5 > a"):
        page = _get_linked_page(region_tag, "")  # href of region tag includes subdomain
        if page:
            region_pages.append(page)

    return region_pages


# Retrieves ad listings from nested sitemap>region>category structure.
def adultsearch_com(html):
    sitemap_soup = BeautifulSoup(html, "html.parser")
    ad_listing_links = []

    region_pages = get_region_pages(sitemap_soup)
    category_pages = get_category_pages(region_pages)

    # Each category page links to city-specific ad listings.
    for page in category_pages:
        sub_domain = _find_domain(page)
        city_list = page.select_one(".city-list").select_one(".row")

        for city_tag in city_list.select("div > a"):
            full_listing_url = urljoin(sub_domain, city_tag.get("href"))
            ad_listing_links.append(full_listing_url)

    return ad_listing_links


# Member methods

# Catches country subdomains, since the main sitemap and US uses the primary adultsearch.com
# but subsequent pages in other countries prepend their URLs.
def _find_domain(soup):
    uri = urlparse(soup.find("link", rel="canonical").get("href"))

    return f"{uri.scheme}://{uri.netloc}"


# Attempt to retrieve the linked page.
def _get_linked_page(link, domain):
    resp = requests.get(urljoin(domain, link.get("href")))

    if resp:
        return BeautifulSoup(resp.text, "html.parser")
