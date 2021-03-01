import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup

categories = [
    "escorts",
    "female-escorts",
    "massage-body-rubs",
    "male-escorts",
    "trans-shemale-escorts",
    "fetish-domination"
]

def sumosear_ch(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    locations = soup.find("a", class_="location-bar__location-btn location-btn js-modal-opener").get("data-full-tags")
    locations = json.loads(locations)
    for _, location_tag in locations:
        for tag in categories:
            links.append(f"https://sumosear.ch/images/tags/{location_tag}/{tag}")
    return links
