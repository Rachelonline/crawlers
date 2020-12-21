from typing import List
from __app__.adparser.sites.base_ad_parser import BaseAdParser
import re

class BackPage_ly(BaseAdParser):
    def primary_phone_number(self) -> str:
        number = self.soup.find("a", class_="mobile")
        if number:
            number = number.get("data-phone")
        #print(number)
        return number

    def phone_numbers(self) -> List:
        return None

    def date_posted(self) -> str:
        date = self.soup.find("i", class_="ad-date").find("span", class_= "utc_time").get_text()
        #print(date)
        return date

    def name(self) -> str:
        return None

    def primary_email(self) -> str:
        return None

    def emails(self) -> List:
        emails = []
        words = self.ad_text().split(" ")
        for word in words:
            if ".com" in word.lower() and "@" in word.lower():
                emails.append(word)
        #print(emails)
        return(emails)

    def social(self) -> List:
        socials = []
        words = self.ad_text().split(" ")
        for word in words:
            if ".com" not in word.lower() and "@" in word.lower():
                socials.append(word)
        #print(socials)
        return(socials)

    def age(self) -> str:
        age = self.ad_title().split(" - ")[1]
        #print(age)
        return age

    def image_urls(self) -> List:
        image_urls = []
        for image in self.soup.findAll("a", class_="image-block"):
            image_urls.append(image.get("href"))
        #print(image_urls)
        return image_urls

    def location(self) -> str:
        category_names = [
            "Escorts", 
            "Body Rubs", 
            "Strippers", 
            "Dom and Fetishes", 
            "Phone & Websites", 
            "Adult Industry Jobs", 
            "Cam Sex", 
            "Women looking for Men", 
            "Men looking for Women", 
            "Men looking for Men", 
            "Women looking for Women", 
            "Friendship - Activity Partners", 
            "Casual Connections"
        ]
        location = self.soup.find("title").get_text().replace(" - BackPage(ly)", "")
        for name in category_names:
            location = location.replace(name, "")
        location = location.replace("BackPage(ly)  ", "")
        #print(location)
        return location

    def ethnicity(self) -> str:
        return None

    def gender(self) -> str:
        return None

    def services(self) -> List:
        return None

    def website(self) -> str:
        websites = []
        words = self.ad_text().split(" ")
        for word in words:
            if ".com" in word.lower() and "@" not in word.lower():
                websites.append(word)
        #print(websites)
        return(websites)

    def ad_text(self) -> str:
        text = self.soup.find("p", class_="description")
        if (text):
            text = text.get_text().replace("\n\n\n\n\nShare", "").replace("\n", "").replace("\t", "")
        #print(text)
        return text

    '''
    def text_info(self) -> str:
        websites = []
        socials = []
        emails = []
        total = []
        words = self.ad_text().split(" ")
        for word in words:
            word = word.lower()
            if ".com" in word and "@" not in word:
                websites.append(word)
            elif ".com" not in word and "@" in word:
                socials.append(word)
            elif ".com" in word and "@" in word:
                emails.append(word)
        total.append(websites)
        total.append(socials)
        total.append(emails)
        return total
    '''
    def ad_title(self) -> str:
        title = self.soup.find("div", class_=['mx-3', 'content', 'clearfix'])
        if (title):
            title = title.find("strong").get_text()
        #print(title)
        return title

    def orientation(self) -> str:
        return None

    def __attributes(self, fieldName) -> str:
        return None