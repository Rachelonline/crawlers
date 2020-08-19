from typing import List
import re
from bs4 import BeautifulSoup

# US and international - consider using phonenumbers lib instead
PHONE_RE = re.compile(
    r"(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?"  # pylint: disable=line-too-long
)

# Basic - could use RFC 5322 instead
EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


class BaseAdParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")
        self.email_re = EMAIL_RE
        self.phone_re = PHONE_RE

    def primary_phone_number(self) -> str:
        raise NotImplementedError

    def phone_numbers(self) -> List:
        raise NotImplementedError

    def date_posted(self) -> str:
        raise NotImplementedError

    def name(self) -> str:
        raise NotImplementedError

    def primary_email(self) -> str:
        raise NotImplementedError

    def emails(self) -> List:
        raise NotImplementedError

    def social(self) -> List:
        raise NotImplementedError

    def age(self) -> str:
        raise NotImplementedError

    def image_urls(self) -> List:
        raise NotImplementedError

    def location(self) -> str:
        raise NotImplementedError

    def ethnicity(self) -> str:
        raise NotImplementedError

    def gender(self) -> str:
        raise NotImplementedError

    def services(self) -> List:
        raise NotImplementedError

    def website(self) -> str:
        raise NotImplementedError

    def ad_text(self) -> str:
        raise NotImplementedError

    def ad_title(self) -> str:
        raise NotImplementedError

    def orientation(self) -> str:
        raise NotImplementedError

    # Only on BaseAdParser, not extended.
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
        }
        return {k: v for k, v in full_ad_dict.items() if v}
