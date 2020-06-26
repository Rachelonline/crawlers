from typing import List
from __app__.adparser.sites.base_ad_parser import BaseAdParser
import re

class BedPage_com(BaseAdParser):
    def primary_phone_number(self) -> str:
        return self.__attributes("Mobile")

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        prim_phone_number = self.primary_phone_number()
        if prim_phone_number:
            phone_numbers_found.append(prim_phone_number)
        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        post_id = self.__attributes("Post ID")
        phone_numbers_found = list(filter((post_id).__ne__, phone_numbers_found))
        return phone_numbers_found

    def date_posted(self) -> str:
        return self.__attributes("Posted")

    def name(self) -> str:
        return None

    def primary_email(self) -> str:
        return self.__attributes("Email")

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
        return self.__attributes("age")

    def image_urls(self) -> List:
        return None

    def location(self) -> str:
        return self.__attributes("Location")

    def ethnicity(self) -> str:
        return None

    def gender(self) -> str:
        return None

    def services(self) -> List:
        return None

    def website(self) -> str:
        return None

    def ad_text(self) -> str:
        content = self.soup.select_one("div#pageBackground").get_text().replace("\n"," ").replace("\t", "").replace("\xa0", "")
        return content

    def ad_title(self) -> str:
        return self.soup.title.string

    def orientation(self) -> str:
        return None

    def __attributes(self, fieldName) -> str:
        text = self.soup.find(text=re.compile(f"{fieldName}:.*"))
        if text:
            value = re.search(r".*:\s+(.+)", text, re.MULTILINE)
            if value:
                return value.group(1).strip()
