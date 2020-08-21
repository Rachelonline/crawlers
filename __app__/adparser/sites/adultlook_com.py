import re
from typing import List
from __app__.adparser.sites.base_ad_parser import BaseAdParser

GENDER_MAPPING = {"Female": "female", "Transsexual": "trans", "Male": "male"}

SERVICE_MAPPING = {
    "Massage": "massage",
    "Body Rubs": "massage",
    "Domination": "bdsm",
    "Escort": "escort",
}


class AdultLook_com(BaseAdParser):
    def primary_phone_number(self) -> str:
        phone_number = self._get_contact_info().find(text=self.phone_re)
        if phone_number:
            return phone_number.strip()
        else:
            return None

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        prim_phone_number = self.primary_phone_number()
        if prim_phone_number:
            phone_numbers_found.append(prim_phone_number)

        matches = self._get_contact_info().find_all(text=self.phone_re)
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        # No dates found on page
        return None

    def name(self) -> str:
        title = self.soup.select_one(".profile-h1")
        if title:
            return title.text.strip()
        else:
            return None

    def primary_email(self) -> str:
        email = self._get_contact_info().find(text=self.email_re)
        if email:
            return email.strip()
        else:
            return None

    def emails(self) -> List:
        emails_found = []
        prim_email = self.primary_email()
        if prim_email:
            emails_found.append(prim_email)

        matches = self._get_contact_info().find_all(text=self.email_re)
        emails_found.extend(["".join(match) for match in matches])
        return emails_found

    def social(self) -> List:
        twitter_accts = self._get_contact_info().find_all(text=re.compile(r"^@\S+"))
        return [re.search(r"^@\S+", acct).group(0) for acct in twitter_accts]

    def age(self) -> str:
        return self._get_profile().get("Age")

    def image_urls(self) -> List:
        images_carousel = self.soup.select_one("#carousel")
        return [img["src"] for img in images_carousel.find_all("img")]

    def location(self) -> str:
        # Assumes city, state is group 1
        loc_regex = r"([A-Za-z]+,\s?[A-Za-z]+).*"
        loc = re.search(loc_regex, self._get_current_info())

        if loc:
            return loc.group(1)

    def ethnicity(self) -> str:
        return self._get_profile().get("Ethnicity")

    def gender(self) -> str:
        current_info_text = self._get_current_info()

        if current_info_text:
            for key in GENDER_MAPPING:
                if key in current_info_text:
                    return GENDER_MAPPING[key]

    def services(self) -> List:
        services = []
        current_info_text = self._get_current_info()

        if current_info_text:
            for key in SERVICE_MAPPING:
                if key in current_info_text:
                    services.append(SERVICE_MAPPING[key])

        if len(services):
            return services
        else:
            return None

    def website(self) -> str:
        website_text = self._get_contact_info().find(text=re.compile(r"Website"))
        if website_text:
            website_link = website_text.find_next("span").find("a").get("href")
            return website_link

    def ad_text(self) -> str:
        ad_text = self.soup.find("blockquote")
        if ad_text:
            return ad_text.text.replace("\n", "").strip()

    def ad_title(self) -> str:
        title = self.soup.select("head > title")
        if len(title) > 0:
            return title[0].text.strip()
        else:  # failed select returns []
            return None

    def orientation(self) -> str:
        return self._get_profile().get("Orientation")

    # Member methods
    def _get_current_info(self) -> str:  # Most recent item in City/Category section
        # Each item in section looks like <City>, <State> <Services>
        category_info_header = self.soup.find(text=re.compile("City / Category"))

        if category_info_header:  # small number of ads do not contain this section
            current_info = (
                category_info_header.find_parent().find_next_sibling().find("a").text
            )
            return current_info.strip()
        else:
            return ""

    def _get_contact_info(self):
        contact_info = self.soup.select_one(
            ".pro-section"
        ).find_next_sibling()  # First profile section
        return contact_info

    def _get_profile(self):
        profile_elem = self.soup.select_one(".portfolio").find_parent()
        profile_info = {
            match.group(1).strip(): match.group(2).strip()
            for match in re.finditer(r"(.*):(.*)", profile_elem.text)
        }

        return profile_info
