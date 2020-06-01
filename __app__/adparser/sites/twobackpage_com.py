from urllib.parse import urljoin
from typing import List
import re
from __app__.adparser.sites.base_ad_parser import BaseAdParser

# TODO: duplicated with adlistingparser
# We dont wan't to include these in the extracted location string
REMOVE_FROM_LOCATATION_STR = set(
    [
        "Home",
        "Africa",
        "Asia, Pacific, and Middle East",
        "Australia and Oceania",
        "Europe",
        "Latin America and Caribbean",
        " >",
        "Adult Jobs",
        "Bodyrubs",
        "Dom and Fetish",
        "Male Escorts",
        "TS",
        "Phone & Websites",
        "Strippers and strip Clubs",
        "Escorts",
        "Male",
    ]
)

GENDER_MAPPING = {"Male": "male", "TS": "trans"}

SERVICES_MAPPING = {
    "Adult Jobs": "adult jobs",
    "Bodyrubs": "Bodyrubs",
    "Dom and Fetish": "dom and fetish",
    "Escorts": "escorts",
    "Male Escorts": "escorts",
    "TS": "escorts",
    "Phone & Websites": "phone & websites",
    "Strippers and strip Clubs": "strippers and strip clubs",
}


class TwoBackpage(BaseAdParser):
    gender_lookup = {"female-escorts": "female", "male-escorts": "male", "ts": "trans"}
    def _buttons(self) -> List:
        links = []
        tapbox = self.soup.find("div", class_="tapbox")
        if tapbox:
            for link in tapbox.find_all("a"):
                links.append(link["href"])
        return links

    def primary_phone_number(self) -> str:
        for link in self._buttons():
            if link.startswith("tel:"):
                return link.replace("tel:", "")


    def phone_numbers(self) -> List:
        phone_numbers_found = []
        prim_phone_number = self.primary_phone_number()
        if prim_phone_number:
            phone_numbers_found.append(prim_phone_number)
        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        posted = self.soup.find("div", class_="adInfo")
        if posted:
            return posted.text.replace("Posted:", "").strip()

    def name(self) -> str:
        return None

    def primary_email(self) -> str:
        for link in self._buttons():
            if link.startswith("mailto:"):
                return link.replace("mailto:", "")

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
        age = re.search(r"Poster age:\s+(\d+)", self.ad_text(), re.MULTILINE)
        if age:
            return age.group(1)

    def image_urls(self) -> List:
        urls = []
        image_div = self.soup.find("ul", id="viewAdPhotoLayout")
        images = image_div("img", src=True) or []
        for image in images:
            urls.append(image["src"])
        return urls

    def location(self) -> str:
        breadcrumb = self.soup.find("div", id="cookieCrumb")
        if breadcrumb:
            location = " ".join(breadcrumb.stripped_strings)

            # Location
            for remove in REMOVE_FROM_LOCATATION_STR:
                location = location.replace(remove, "")
            if location:
                loc_text = re.search(r"Location:\s+(.*)\n", self.ad_text(), re.MULTILINE)
                if loc_text:
                    location = f"{location.strip()} {loc_text.group(1).strip()}"
                return location.strip()

    def ethnicity(self) -> str:
        return None

    def gender(self) -> str:
        breadcrumb = self.soup.find("div", id="cookieCrumb")
        if breadcrumb:
            location = " ".join(breadcrumb.stripped_strings)

            # Gender
            for k, v in GENDER_MAPPING.items():
                if k in location:
                    return v
        return "female"

    def services(self) -> List:
        breadcrumb = self.soup.find("div", id="cookieCrumb")
        if breadcrumb:
            location = " ".join(breadcrumb.stripped_strings)
            # Service
            for k, v in SERVICES_MAPPING.items():
                if k in location:
                    return [v]

    def website(self) -> str:
        return None

    def ad_text(self) -> str:
        content = "\n".join(
            string
            for string in self.soup.find("div", class_="mainBody").stripped_strings
        ).replace(u"\xa0", "")
        if content:
            return content


    def ad_title(self) -> str:
        return self.soup.find("div", id="postingTitle").text.strip()

    def orientation(self) -> str:
        return None
