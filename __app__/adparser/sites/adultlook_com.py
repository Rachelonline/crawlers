import re
from typing import List
from __app__.adparser.sites.base_ad_parser import BaseAdParser


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
        return self._get_profile().get("Age", "")

    def image_urls(self) -> List:
        # Gets First element on page, assumes every link is to an image
        images_set = self.soup.select_one(
            "#ppage > div > div > div:nth-child(6) > div:nth-child(1)"
        )
        return [img["src"] for img in images_set.select("img")]

    def location(self) -> str:
        # Gets Third element on page, assumes city name is first group of string.
        location_elem = self.soup.select_one(
            "#ppage > div > div > div:nth-child(6) > div:nth-child(3)"
        )
        loc = location_elem.find("div")
        if loc:
            loc_string = loc.text.strip()
            loc_regex = r"([A-Za-z]+,\s?[A-Za-z]+).*"
            return re.search(loc_regex, loc_string).group(1)
        else:
            return None

    def ethnicity(self) -> str:
        return self._get_profile().get("Ethnicity", "")

    def gender(self) -> str:
        return self._get_profile().get("Gender", "")

    def services(self) -> List:
        return []

    def website(self) -> str:
        emails = self._get_contact_info().find(text=re.compile(r"[^@]+.[a-z]+"))
        if len(emails) > 0:
            primary, *_ = emails
            return primary.strip()
        else:
            return None

    def ad_text(self) -> str:
        ad_text = self.soup.select_one("#ppage > div > div > div:nth-child(8)")
        return ad_text.text.replace("\n", "").strip()

    def ad_title(self) -> str:
        title = self.soup.select("head > title")
        if len(title) > 0:
            return title[0].text.strip()
        else:
            return None

    def orientation(self) -> str:
        return self._get_profile().get("Orientation", "")

    # Member methods
    def _get_contact_info(self):
        # Gets second element on page, assumes it contains main contact info
        contact_info = self.soup.select_one(
            "#ppage > div > div > div:nth-child(6) > div:nth-child(2)"
        )
        return contact_info

    def _get_profile(self):
        # Gets fourth element on page, assumes it contains profile-based information (in a key: value format)
        profile_elem = self.soup.select_one(
            "#ppage > div > div > div:nth-child(6) > div:nth-child(4)"
        )

        profile_info = {
            mat.group(1).strip(): mat.group(2).strip()
            for mat in re.finditer(r"(.*):(.*)", profile_elem.text)
        }
        return profile_info
