from urllib.parse import urljoin
from typing import List
import re
from __app__.adparser.sites.base_ad_parser import BaseAdParser


class OneBackPage_com(BaseAdParser):
    gender_lookup = {"female escorts": "female", "trans escorts": "trans"}

    def primary_phone_number(self) -> str:
        tags = self.soup.find_all("i", class_="fa fa-user-circle")

        if len(tags) > 1:
            return tags[1].next.replace(":", "").strip()

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

    def primary_email(self) -> str:
        return None

    def emails(self) -> List:
        emails_found = []
        matches = self.email_re.findall(self.ad_text())
        emails_found.extend(["".join(match) for match in matches])
        return emails_found

    def social(self) -> List:
        text = self.soup.find(text=re.compile(f"Social Link.*:.*"))

        if text:
            links = text.parent.find_all("a")
            return list(map(lambda a: a["href"], links))

    def age(self) -> str:
        return self.__attributes("Age")

    def image_urls(self) -> List:
        urls = []
        images = self.soup.find_all("div", class_="item galleryz slide")
        for image in images:
            urls.append(image.find_all("a")[0]["href"])
        return urls

    def location(self) -> str:
        return self.__attributes("Location")

    def ethnicity(self) -> str:
        return None

    def gender(self) -> str:
        gender = self.__attributes("Category")
        return self.gender_lookup.get(gender.lower(), "unknown")

    def services(self) -> List:
        return [self.__attributes("Category")]

    def website(self) -> str:
        return None

    def ad_text(self) -> str:
        header = self.soup.find(class_="desss")
        if header:
            tags = header.parent.find_all("p")
            description = ""
            for tag in tags:
                if tag.find("script"):
                    continue
                description += (
                    "\n".join(string for string in tag.stripped_strings).replace(
                        "\xa0", ""
                    )
                    + "\n"
                )
            return description

    def ad_title(self) -> str:
        return self.soup.find_all("h1", class_="judul")[0].text

    def orientation(self) -> str:
        return None

    def __attributes(self, fieldName) -> str:
        text = self.soup.find(text=re.compile(f"{fieldName}:.*"))
        if text:
            value = re.search(r".*:\s+(.+)\s+", text, re.MULTILINE)
            if value:
                return value.group(1).strip()
