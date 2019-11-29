import re
from urllib.parse import urljoin
from typing import List
from __app__.adparser.sites.base_ad_parser import BaseAdParser
from datetime import datetime


class EscortDirectory(BaseAdParser):
    def primary_phone_number(self) -> str:
        wrapper = self.soup.find(class_="phone-data-wrapper")
        return wrapper.find(class_="phone").string.strip()

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        primary_phone_number = self.primary_phone_number()
        if primary_phone_number:
            phone_numbers_found.append(primary_phone_number)
        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        details = self.soup.find(class_="escort-details")
        text = details.find(text=re.compile("Last modified")).string
        modified_date = re.search(r"(\d+/\d+/\d+)", text)
        return datetime.strptime(modified_date.group(), "%d/%m/%Y").isoformat()

    def name(self) -> str:
        wrapper = self.soup.find(class_="group-details-container")
        return wrapper.find(class_="name").contents[0].strip()

    def primary_email(self) -> str:
        return None

    def emails(self) -> List:
        return None

    def social(self) -> List:
        return None

    def age(self) -> str:
        return self.__attributes("Age: ")

    def image_urls(self) -> List:
        urls = []
        wrapper = self.soup.find(id="modalCarousel-gallery")
        images = wrapper.find_all("img")
        for image in images:
            urls.append(image["src"])
        return urls

    def location(self) -> str:
        wrapper = self.soup.find(class_="info-container").find(class_="info")
        content = " ".join(
            tag.string.strip() for tag in wrapper.find_all("a", class_="text-brown")
        )
        if content:
            return content

    def ethnicity(self) -> str:
        return self.__attributes("Ethnic: ")

    def gender(self) -> str:
        return self.__attributes("Gender: ")

    def services(self) -> List:
        wrapper = self.soup.find(class_="sedcard-showname")
        if wrapper:
            service = wrapper.text.split()[0]
            return [service]

    def website(self) -> str:
        wrapper = self.soup.select("div.buttons-container.contact-note")[0]
        website_text = wrapper.find(text=re.compile(r"Website", re.IGNORECASE))
        if website_text:
            website_link = website_text.find_parent("a")["href"]
            link_index = website_link.find("link=")
            if link_index > -1:
                link_index += len("link=")
                return website_link[link_index:]
            else:
                return website_link

    def ad_text(self) -> str:
        wrapper = self.soup.find(class_="escort-details")
        content = "\n".join(string for string in wrapper.stripped_strings)
        if content:
            return content

    def ad_title(self) -> str:
        return self.soup.find("title").string.strip()

    def orientation(self) -> str:
        return self.__attributes("Orientation: ")

    def __attributes(self, fieldName) -> str:
        wrapper = self.soup.find(class_="personal-details")
        label = wrapper.find(text=fieldName)
        if label:
            return label.parent.find_next_siblings()[0].string.strip()
