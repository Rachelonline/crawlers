from typing import List
from __app__.adparser.sites.base_ad_parser import BaseAdParser
import re

class SumoSear_ch(BaseAdParser):
    def primary_phone_number(self) -> str:
        number = self.soup.find("a", class_="card-info__tel-num")
        if number:
            return number.get_text()

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        phone_number_primary = self.primary_phone_number()
        if phone_number_primary:
            phone_numbers_found.append(phone_number_primary)
        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        date = self.soup.find("time")
        if date:
            return date.get("datetime")

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
        return None

    def age(self) -> str:
        return self.__attributes("Age: ")

    def image_urls(self) -> List:
        image_urls = []
        for image in self.soup.findAll("figure", class_="i-gallery__thumb js-gallery__item"):
            image_urls.append(image.get("data-picture-src"))
        return image_urls

    def location(self) -> str:
        return self.__attributes("Location: ")

    def ethnicity(self) -> str:
        return None

    def gender(self) -> str:
        return None

    def services(self) -> List:
        return None

    def website(self) -> str:
        return None

    def ad_text(self) -> str:
        text = self.soup.find("div", class_="card-info__secondary")
        if text:
            return text.get_text()

    def ad_title(self) -> str:
        title = self.soup.find("div", class_="card-info__primary")
        if title:
            return title.get_text()

    def orientation(self) -> str:
        return None

    def __attributes(self, fieldName) -> str:
        attributes = self.soup.findAll("span", class_="data-attrs__item")
        for attribute in attributes:
            if fieldName in attribute.get_text():
                return attribute.get_text().replace(fieldName, "")
