from urllib.parse import urljoin
from typing import List
import re
from __app__.adparser.sites.base_ad_parser import BaseAdParser


class OneBackPage_com(BaseAdParser):
    gender_lookup = {"female-escorts": "female", "male-escorts": "male", "ts": "trans"}

    def primary_phone_number(self) -> str:
        return (
            self.soup.find_all("i", class_="fa fa-user-circle")[1]
            .next.replace(":", "")
            .strip()
        )

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        prim_phone_number = self.primary_phone_number()
        if prim_phone_number:
            phone_numbers_found.append(prim_phone_number)
        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        return self.soup.find_all("span", class_="utc_time")[0].text

    def name(self) -> str:
        return None

    def emails(self) -> List:
        emails_found = []
        prim_email = self.primary_email()
        if prim_email:
            emails_found.append(prim_email)
        matches = self.email_re.findall(self.ad_text())
        emails_found.extend(["".join(match) for match in matches])
        return emails_found

    def social(self) -> List:
        return None

    def age(self) -> str:
        age = re.search(r"Age:\s+(\d+)", self.ad_text(), re.MULTILINE)
        if age:
            return age.group(1)

    def image_urls(self) -> List:
        urls = []
        images = self.soup.find_all("div", class_="item galleryz slide")
        for image in images:
            urls.append(image.find_all("a")[0]["href"])
        return urls

    def location(self) -> str:
        return self.soup.find_all("i", class_="fa fa-user-circle")[0].next.strip()

    def ethnicity(self) -> str:
        return None

    def gender(self) -> str:
        gender = (
            self.soup.find_all("i", class_="fa fa-chevron-down")[0]
            .next.replace("Category: ", "")
            .strip()
        )
        if "female" in gender.lower():
            return "female"
        elif "male" in gender.lower():
            return "male"
        else:
            return None

    def services(self) -> List:
        return None

    def website(self) -> str:
        return None

    def ad_text(self) -> str:
        return self.soup.find_all("h4", class_="desss")[0].next.next.next.text.strip()

    def ad_title(self) -> str:
        return self.soup.find_all("h1", class_="judul")[0].text

    def orientation(self) -> str:
        return None
