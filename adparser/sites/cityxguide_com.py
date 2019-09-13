from urllib.parse import urljoin
from typing import List
from adparser.sites.base_ad_parser import BaseAdParser


class CityXGuide(BaseAdParser):
    gender_lookup = {"female-escorts": "female", "male-escorts": "male", "ts": "trans"}

    def primary_phone_number(self) -> str:
        phone_str = self.soup.find("span", class_="_phone").string
        if phone_str != "Not Available":
            return phone_str

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        prim_phone_number = self.primary_phone_number()
        if prim_phone_number:
            phone_numbers_found.append(prim_phone_number)
        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        posted = self.soup.find("span", text="Last Updated").next_sibling
        return posted.string

    def name(self) -> str:
        name_str = self.soup.find("span", class_="_name").text
        if "not available" not in name_str.lower():
            return name_str

    def primary_email(self) -> str:
        email_str = self.soup.find("span", class_="_email").string
        if email_str != "Not Available":
            return email_str

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
        age_str = self.soup.find("span", class_="_age").string
        if age_str != "Not Available":
            return age_str

    def image_urls(self) -> List:
        urls = []
        image_div = self.soup.find("div", class_="swiper-wrapper")
        images = image_div("img", src=True) or []
        for image in images:
            urls.append(urljoin("http:", image["src"]))
        return urls

    def location(self) -> str:
        location_str = self.soup.find("span", class_="_location").string
        if location_str != "Not Available":
            return location_str

    def ethnicity(self) -> str:
        ethnicity_span = self.soup.find("span", class_="_ethnicity")
        if ethnicity_span and ethnicity_span.string != "Not Available":
            return ethnicity_span.string

    def gender(self) -> str:
        category = self.soup.find("span", text="Category").next_sibling
        link = category.find("a").get("href")
        gender = self.gender_lookup.get(link.split('/')[-1], "unknown")
        return gender

    def services(self) -> List:
        return None

    def website(self) -> str:
        website_span = self.soup.find("span", class_="_website")
        if website_span and website_span.string != "Not Available":
            return website_span.string

    def ad_text(self) -> str:
        content = "\n".join(
            string
            for string in self.soup.find("div", class_="section-page").stripped_strings
        )
        if content:
            return content

    def ad_title(self) -> str:
        return self.soup.find("h1", itemprop="name").string
