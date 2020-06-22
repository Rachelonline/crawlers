import re
from typing import List
import pprint
from __app__.adparser.sites.base_ad_parser import BaseAdParser


class AdultLookParser(BaseAdParser):

    @property
    def _adult_finder_phone_regex(self):
        return re.compile(r"[0-9]{3}-[0-9]{3}-[0-9]{4}")

    def _load_common_components(self):
        # Loads commonly used components of a given advert
        self._contact_info = self._get_contact_info()
        self._profile = self._get_profile()

    def _get_contact_info(self):
        # Gets second element on page, assumes it contains main contact info
        expecting_one = self.soup.select("#ppage > div > div > div:nth-child(6) > div:nth-child(2)")
        assert (len(expecting_one) == 1)

        contact_info, *_ = expecting_one
        return contact_info

    def _get_profile(self):
        # Gets fourth element on page, assumes it contains profile-based information (in a key: value format)
        expecting_one = self.soup.select("#ppage > div > div > div:nth-child(6) > div:nth-child(4)")
        assert (len(expecting_one) == 1)
        profile_elem, *_ = expecting_one

        profile_info = {mat.group(1).strip(): mat.group(2).strip() for mat in
                        re.finditer(r"(.*):(.*)", profile_elem.text)}
        return profile_info

    def ad_dict(self) -> dict:
        self._load_common_components()
        return super(self.__class__, self).ad_dict()

    # Implemented Methods
    def primary_phone_number(self) -> str:
        phone_number = self._contact_info.find(text=self._adult_finder_phone_regex)
        if phone_number:
            return phone_number.strip()
        else:
            return ""

    def phone_numbers(self) -> List:
        phone_numbers = self.soup.findAll(text=self._adult_finder_phone_regex)
        return list(set([re.search(self._adult_finder_phone_regex, pn).group(0) for pn in phone_numbers]))

    def date_posted(self) -> str:
        # No dates found on page
        return ""

    def name(self) -> str:
        title = self.soup.select_one(".profile-h1")
        if title:
            return title.text.strip()
        else:
            return ""

    def primary_email(self) -> str:
        email = self._contact_info.find(text=self.email_re)
        if email:
            return email.strip()
        else:
            return ""

    def emails(self) -> List:
        emails = self.soup.findAll(text=self.email_re)
        return list(set([re.search(self.email_re, email).group(0) for email in emails]))

    def social(self) -> List:
        twitter_accts = self._contact_info.findAll(text=re.compile(r"^@\S+"))
        return list(set([re.search(r"^@\S+", acct).group(0) for acct in twitter_accts]))

    def age(self) -> str:
        return self._profile.get('Age', "")

    def image_urls(self) -> List:
        # Gets First element on page, assumes every link is to an image
        expecting_one = self.soup.select("#ppage > div > div > div:nth-child(6) > div:nth-child(1)")
        assert (len(expecting_one) == 1)

        images_set, *_ = expecting_one

        return [img['src'] for img in images_set.select("img")]

    def location(self) -> str:
        # Gets Third element on page, assumes city name is first group of string.
        expecting_one = self.soup.select("#ppage > div > div > div:nth-child(6) > div:nth-child(3)")
        assert (len(expecting_one) == 1)
        location_elem, *_ = expecting_one

        loc = location_elem.find('div')
        if loc:
            loc_string = loc.text.strip()
            loc_regex = r'([A-Za-z]+,\s?[A-Za-z]+).*'
            return re.search(loc_regex, loc_string).group(1)
        else:
            return ""

    def ethnicity(self) -> str:
        return self._profile.get('Ethnicity', "")

    def gender(self) -> str:
        return self._profile.get('Gender', "")

    def services(self) -> List:
        return []

    def website(self) -> str:
        emails = self._contact_info.find(text=re.compile(r"[^@]+.[a-z]+"))
        if len(emails) > 0:
            primary, *_ = emails
            return primary.strip()
        else:
            return ""

    def ad_text(self) -> str:
        expecting_one = self.soup.select("#ppage > div > div > div:nth-child(8)")
        assert (len(expecting_one) == 1)
        ad_text, *_ = expecting_one
        return ad_text.text.replace('\n', '').strip()

    def ad_title(self) -> str:
        title = self.soup.select("head > title")
        if len(title) > 0:
            return title[0].text.strip()
        else:
            return ""

    def orientation(self) -> str:
        return self._profile.get('Orientation', "")
