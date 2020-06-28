from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

_domain = "https://adultlook.com/"


def adultlook(html: str) -> [str]:
    """
    Fetches adlisting urls from adultlook.com

    Since adultlook.com doesn't provide a top-level listing. One needs to iterate through the
    listing tree until "leafs" are reached -- which will be our adlisting pages.
    :param html: HTML text of starting page
    :return: List of URLs
    """
    soups = [BeautifulSoup(html, "html.parser")]
    leaves = []
    count = 0
    while soups:
        soup, *soups = soups
        for res in _yield_next_links(soup):
            is_leaf, link = res
            if is_leaf:
                leaves.append(link)
            else:
                soups.extend(_get_page(link))
            count += 1
    return leaves


def _yield_next_links(soup):
    # If our breadcrumb is 4 wide, this is a leaf
    breadcrumb_size = _get_breadcrumb_size(soup)
    if breadcrumb_size > 3:
        return

    maybe_grid = soup.select(".grid > div")
    maybe_container = soup.select(".container > div:nth-child(6)")
    if maybe_grid:
        for listing in _handle_grid_page(maybe_grid):
            yield breadcrumb_size + 1 > 3, listing
    elif maybe_container:
        for listing in _handle_container_page(maybe_container):
            yield breadcrumb_size + 1 > 3, listing


def _get_breadcrumb_size(soup):
    maybe_breadcrumb = soup.find(class_="breadcrumb")
    if maybe_breadcrumb:
        return len(maybe_breadcrumb.find_all("li", recursive=False))
    else:
        return 0


def _handle_grid_page(grid):
    for sublisting in grid:
        for listing in (urljoin(_domain, link["href"]) for link in sublisting.select("a") if link.has_attr("href")):
            yield listing


def _handle_container_page(container):
    for sublisting in container:
        for listing in (urljoin(_domain, link["href"]) for link in sublisting.select("a") if link.has_attr("href")):
            yield listing


def _get_page(link):
    r = requests.get(link)
    if r:
        return [BeautifulSoup(r.text)]
    else:
        return []


if __name__ == "__main__":
    print(adultlook(requests.get(_domain).text))
