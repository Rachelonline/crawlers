from urllib.parse import urljoin
from typing import List
import re
from bs4 import BeautifulSoup
from __app__.adparser.sites.base_ad_parser import BaseAdParser


# US and international - consider using phonenumbers lib instead
PHONE_RE = re.compile(
    r"(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?"  # pylint: disable=line-too-long
)

# Basic - could use RFC 5322 instead
EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


class Backpagely(BaseAdParser):
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")
        self.email_re = EMAIL_RE
        self.phone_re = PHONE_RE

    def primary_phone_number(self) -> str:
        phone_strs = soup.find("li")
        for li in phone_strs:
            if 'Phone :' in li.text:
                return li

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        prim_phone_number = self.primary_phone_number()
        if prim_phone_number:
            phone_numbers_found.append(prim_phone_number)

        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        return self.soup.find("i", class_="ad-date")

    def name(self) -> str:
        return None

    def primary_email(self) -> str:
        return None

    def emails(self) -> List:
        emails_found = []
    
        matches = self.email_re.findall(self.ad_text())
        emails_found.extend(["".join(match) for match in matches])
        return emails_found

    def social(self) -> List:
        content = self.ad_text()
        raise NotImplementedError

    def age(self) -> str:
        title = self.ad_title()
        if '-' in title:
            age = title.split('-')[1].strip()
        else:
            age = None
        return age
        
    def image_urls(self) -> List:
        image_links = self.soup.find_all("a", class_="image-block")
        urls = [link["href"] for link in image_links]
        return urls

    def location(self) -> str:
        raise NotImplementedError

    def ethnicity(self) -> str:
        raise NotImplementedError

    def gender(self) -> str:
        raise NotImplementedError

    def services(self) -> List:
        raise NotImplementedError

    def website(self) -> str:
        return None

    def ad_text(self) -> str:
        text = self.soup.find("p", class_="description")
        if text:
            return text
        else:
            text = self.soup.find_all("p")
        
        return text

    def ad_title(self) -> str:
        return self.soup.find("strong")

    def orientation(self) -> str:
        return None

    # New field added: many posts have a clickable link to share them
    def share_url(self) -> str:
        share_link = self.soup.find("a", class_="ui-button ui-button-middle")
        if share_link:
            url = share_link["href"]
        else:
            url = None

        return url

    def ad_dict(self) -> dict:
        full_ad_dict = {
            "primary-phone-number": self.primary_phone_number(),
            "phone-numbers": self.phone_numbers(),
            "date-posted": self.date_posted(),
            "name": self.name(),
            "primary-email": self.primary_email(),
            "emails": self.emails(),
            "social": self.social(),
            "age": self.age(),
            "image-urls": self.image_urls(),
            "location": self.location(),
            "ethnicity": self.ethnicity(),
            "gender": self.gender(),
            "services": self.services(),
            "website": self.website(),
            "ad-text": self.ad_text(),
            "ad-title": self.ad_title(),
            "orientation": self.orientation(),
            "share-url": self.share_url()
        }
        return {k: v for k, v in full_ad_dict.items() if v}
