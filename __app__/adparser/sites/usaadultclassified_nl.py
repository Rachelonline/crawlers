from urllib.parse import urljoin
from typing import List
import re
import copy
from __app__.adparser.sites.base_ad_parser import BaseAdParser

class USAAdultClassified(BaseAdParser):

    def primary_phone_number(self) -> str:
        return self.soup.select('._phone>a')[0].text

    def phone_numbers(self) -> List:
        return [self.primary_phone_number()]

    def _get_header(self) -> str:
        return copy.copy(self.soup.find_all(class_='postheader')[0].find('td'))

    def date_posted(self) -> str:
        header = self._get_header()
        header.b.decompose()
        date = header.text.replace('|', '').replace('\n', '').strip()
        return date

    def name(self) -> str:
        name_soup = self.soup.select('._name')[0]
        name_soup.b.decompose()
        return name_soup.text.strip()

    def primary_email(self) -> str:
        return self.soup.select('._email')[0].text

    def emails(self) -> List:
        return [self.primary_email()]

    def social(self) -> List:
        return []

    def age(self) -> str:
        return self.soup.select('._age')[0].text

    def image_urls(self) -> List:
        return ['https:' + x['src'] for x in self.soup.select('img')]

    def location(self) -> str:
        b = self.soup.find('b', text=re.compile('Current Filters:'))
        return ', '.join([x.text for x in b.find_next_siblings('a')])
        # return self.soup.select('._location')[0].text

    def ethnicity(self) -> str:
        return self.soup.select('.Ethnicity')[0].text

    def gender(self) -> str:
        return ""

    def services(self) -> List:
        return self.soup.select('.Intimate_Activities')[0].text.split(', ')

    def website(self) -> str:
        return ""

    def ad_text(self) -> str:
        return self.soup.select('#wrap>p')[0].text

    def ad_title(self) -> str:
        return self._get_header().find('b').text

    def orientation(self) -> str:
        return ""


