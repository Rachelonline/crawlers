from urllib.parse import urljoin
from datetime import datetime
from typing import List
from __app__.adparser.sites.base_ad_parser import BaseAdParser


def decode_email(encoded_email: str) -> str:
    """ decode the alleged email protection"""

    def sub_str_to_int(string, index):
        return int(string[index : index + 2], 16)

    factor = sub_str_to_int(encoded_email, 0)
    index = 2
    email = ""

    while index < len(encoded_email):
        email += chr(sub_str_to_int(encoded_email, index) ^ factor)
        index += 2
    return email


class GfeMonkey(BaseAdParser):
    gender_lookup = {"female-escorts": "female", "male-escorts": "male", "ts": "trans"}

    def primary_phone_number(self) -> str:
        contact = self.soup.find("div", id="contact")
        if contact:
            phone = contact.find("td", text="Phone:")
            if phone:
                return phone.find_next_sibling("td").text

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        prim_phone_number = self.primary_phone_number()
        if prim_phone_number:
            phone_numbers_found.append(prim_phone_number)
        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        # GFE doesn't have ad posted dates
        return None

    def name(self) -> str:
        return self.ad_title()

    def primary_email(self) -> str:
        contact = self.soup.find("div", id="contact")
        if contact:
            email = contact.find("td", text="Email:")
            if email:
                email_link = email.next_sibling.find("span")
                email_link = email_link.get("data-cfemail")
                if email_link:
                    return decode_email(email_link)

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
        stats = self.soup.find("div", id="stats")
        if stats:
            label = stats.find("td", text="Age:")
            if label:
                return label.find_next_sibling("td").text

    def image_urls(self) -> List:
        urls = []
        image_div = self.soup.find("div", id="carousel")
        if image_div:
            images = image_div("img", src=True, class_=False) or []
            for image in images:
                urls.append(urljoin("https://www.gfemonkey.com", image["src"]))

        return urls

    def location(self) -> str:
        stats = self.soup.find("div", id="stats")
        if stats:
            label = stats.find("td", text="Location:")
            if label:
                return label.find_next_sibling("td").text

    def ethnicity(self) -> str:
        stats = self.soup.find("div", id="stats")
        if stats:
            label = stats.find("td", text="Ethnicity:")
            if label:
                return label.find_next_sibling("td").text

    def gender(self) -> str:
        stats = self.soup.find("div", id="stats")
        if stats:
            label = stats.find("td", text="Gender:")
            if label:
                return label.find_next_sibling("td").text

    def services(self) -> List:
        return None

    def website(self) -> str:
        contact = self.soup.find("div", id="contact")
        if contact:
            website = contact.find("td", text="Website:")
            if website:
                return website.next_sibling.text.strip()

    def ad_text(self) -> str:
        content = "\n".join(
            string
            for string in self.soup.find("div", id="pageContent").stripped_strings
        )
        return content.replace(u"\xa0", u" ")

    def ad_title(self) -> str:
        title = self.soup.find("h2", class_="profile-name")
        return title.text

    def orientation(self) -> str:
        return None
