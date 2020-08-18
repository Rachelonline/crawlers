from typing import List
from __app__.adparser.sites.base_ad_parser import BaseAdParser
import re

class BedPage_com(BaseAdParser):
    def primary_phone_number(self) -> str:
        return self.__attributes("Mobile")

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        phone_number_primary = self.primary_phone_number()
        if phone_number_primary:
            phone_numbers_found.append(phone_number_primary)
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
        email_primary = self.primary_email()
        if email_primary:
            emails_found.append(email_primary)
        matches = self.email_re.findall(self.ad_text())
        emails_found.extend(["".join(match) for match in matches])
        return emails_found

    def social(self) -> List:
        return None

    def age(self) -> str:
        return self.__attributes("age")

    def image_urls(self) -> List:
        image_urls_found = []
        images = self.soup.select("#viewAdPhotoLayout img")
        for img in images:
            image_urls_found.append(img.get('src'))
        return image_urls_found

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
        # Grabs things from the standardized fields at the bottom of the ad
        text = self.soup.find(text=re.compile(f"{fieldName}:.*"))
        if text:
            value = re.search(r".*:\s+(.+)", text, re.MULTILINE)
            if value:
                return value.group(1).strip()
