from typing import List
from __app__.adparser.sites.base_ad_parser import BaseAdParser
import re

class BackPage_ly(BaseAdParser):
    def primary_phone_number(self) -> str:
        number = self.soup.find("a", class_="mobile")
        if number:
            number = number.get("data-phone")
        return number

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        phone_number_primary = self.primary_phone_number()
        if phone_number_primary:
            phone_numbers_found.append(phone_number_primary)
        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        date = self.soup.find("i", class_="ad-date").find("span", class_= "utc_time").get_text()
        return date

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
        socials = []
        words = self.ad_text().split(" ")
        for word in words:
            if ".com" not in word.lower() and "@" in word.lower():
                socials.append(word)
        return(socials)

    def age(self) -> str:
        age = self.ad_title().split(" - ")[1]
        return age

    def image_urls(self) -> List:
        image_urls = []
        for image in self.soup.findAll("a", class_="image-block"):
            image_urls.append(image.get("href"))
        return image_urls

    def location(self) -> str:
        city = self.soup.find("a", class_="breadcrumb city").get_text()
        region = self.soup.find("a", class_="breadcrumb region").get_text()
        country = self.soup.find("a", class_="breadcrumb country").get_text()
        location = city + ", " + region + ", " + country
        return location

    def ethnicity(self) -> str:
        return None

    def gender(self) -> str:
        return None

    def services(self) -> List:
        return None

    def website(self) -> str:
        return None

    def ad_text(self) -> str:
        text = self.soup.find("p", class_="description")
        if (text):
            text = text.get_text().replace("\n\n\n\n\nShare", "").replace("\n", "").replace("\t", "")
        return text

    def ad_title(self) -> str:
        title = self.soup.find("div", class_=['mx-3', 'content', 'clearfix'])
        if (title):
            title = title.find("strong").get_text()
        return title

    def orientation(self) -> str:
        return None

    def __attributes(self, fieldName) -> str:
        return None