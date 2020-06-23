from urllib.parse import urljoin
from bs4 import BeautifulSoup


def usaadultclassified_nl(html):
    return [x['href'] for x in soup.find_all("a", class_="posttitle")]