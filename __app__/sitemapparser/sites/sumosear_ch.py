import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup

#https://sumosear.ch/images/tags/carbondale-il/escorts
#https://sumosear.ch/images/tags/carbondale-il/female-escorts

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
    locations = eval(locations)
    location_tags = []
    for location in locations:
        location_tags.append(location[1])
    for location_tag in location_tags:
        for tag in tags:
            links.append(f"https://sumosear.ch/images/tags/{location_tag}/{tag}")
    return links
