import re
from typing import List, Dict
from __app__.adparser.sites.base_ad_parser import BaseAdParser

GENDER_MAPPING = {"Female": "female", "Shemale": "trans"}


class AdultSearch_com(BaseAdParser):
    # Initialize commonly referenced soup as properties to avoid reconstruction.
    # See implementation at bottom of class.
    def __init__(self, html):
        super().__init__(html)
        self.about_section = self._get_about_section()
        self.breadcrumb = self._get_breadcrumb()

    def primary_phone_number(self) -> str:
        phone_number = self.soup.select_one(".details__heading").find("a")
        return phone_number.text.strip()

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        phone_number_primary = self.primary_phone_number()
        if phone_number_primary:
            phone_numbers_found.append(phone_number_primary)

        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        return None

    def name(self) -> str:
        name = self.soup.select_one(".details__heading").find("span")
        return name.text.strip()

    def primary_email(self) -> str:
        return self.about_section.get("Email")  # did not see any ads with Email here

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
        stats = self.about_section.get("Stats").split(", ")
        if len(stats) > 0:
            return stats[0].strip().replace(" years old", "")

    def image_urls(self) -> List:
        images_carousel = self.soup.select_one("#ad").select_one(".carousel")

        return [("https:" + img["src"]) for img in images_carousel.find_all("img")]

    def location(self) -> str:
        loc_info = self.breadcrumb[:-1]  # all but last category crumb
        extra_loc_info = self.about_section.get("Location")
        if extra_loc_info:
            loc_info.append(extra_loc_info.strip())

        return ", ".join(loc_info)

    def ethnicity(self) -> str:
        stats = self.about_section.get("Stats").split(", ")
        if len(stats) > 1:
            return stats[1].strip()

    def gender(self) -> str:
        category = self.breadcrumb[-1]

        for key in GENDER_MAPPING:
            if key in category:
                return GENDER_MAPPING[key]

    def services(self) -> List:
        services = []
        category = self.breadcrumb[-1]

        if "Massage" in category or self.about_section.get("Massage"):
            services.append("massage")

        if "Escort" in category:
            services.append("escort")

        if self.about_section.get("Fetish Session"):
            services.append("bdsm")

        return services

    def website(self) -> str:
        return self.about_section.get("Website")

    def ad_text(self) -> str:
        description_body = self.soup.select(".details__card-body")[2].find(
            "div"
        )  # last card is description

        if description_body:
            stripped_text = description_body.text.strip()
            for r in (("\n", ""), ("\xa0", " ")):
                stripped_text = stripped_text.replace(*r)

            return stripped_text

    def ad_title(self) -> str:
        heading_items = self.soup.select_one(".details__heading").find_all("span")
        return heading_items[1].text.strip()

    def orientation(self) -> str:
        return self.about_section.get("Available To")

    # Member methods
    def _get_about_section(self) -> Dict:  # contains stats, services
        about_body = self.soup.select_one(
            ".details__card-header", text=re.compile("About")
        ).find_next_sibling()

        about_info = {}

        for row in about_body.find_all("tr"):
            title = row.find("td")
            body = title.find_next_sibling("td")
            about_info[title.text.strip()] = body.text.strip()

        return about_info

    def _get_breadcrumb(self) -> List:
        # Home > Country > State (for CA/US) > Locality > Category > Phone #
        breadcrumb_text = [
            crumb.text.strip()
            for crumb in self.soup.select_one(".breadcrumb").find_all("li")
        ]
        phone_index = len(breadcrumb_text) - 1  # return list with category as last elem

        return breadcrumb_text[1:phone_index]  # exclusive end
