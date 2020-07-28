from urllib.parse import urljoin
from typing import List
from __app__.adparser.sites.base_ad_parser import BaseAdParser


class MegaPersonals(BaseAdParser):
    gender_lookup = {"female-escorts": "female", "male-escorts": "male", "ts": "trans"}

    def primary_phone_number(self) -> str:
        phone_str = self.soup.find("span", class_="toShowPhone")
        if phone_str:
            return phone_str.string

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        prim_phone_number = self.primary_phone_number()
        if prim_phone_number:
            phone_numbers_found.append(prim_phone_number)
        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        # The dates are from the ad listing themselves - we don't have dates in the ads
        return None

    def name(self) -> str:
       city_str = self.soup.find("p", class_="prev_city")
       if city_str:
         name = city_str.find("span", class_="fromRight")
         return name.string.replace("Name: ", "")

    def primary_email(self) -> str:
        return None

    def emails(self) -> List:
        emails_found = []
        matches = self.email_re.findall(self.ad_text())
        emails_found.extend(["".join(match) for match in matches])
        return emails_found

    def social(self) -> List:
        return None

    def age(self) -> str:
        age_str = self.soup.find("div", class_="post_preview_age")
        if age_str:
            age_str = age_str.string.replace("Age:", "")
            return age_str.strip()

    def image_urls(self) -> List:
        urls = []
        image_div = self.soup.find("div", class_="viewpostgallery")
        if image_div:
            images = image_div("img", src=True) or []
            for image in images:
                urls.append(image["src"])

        # we also can have videos !
        videos = self.soup.find_all("source", {"type": "video/mp4"})
        for video in videos:
            urls.append(video["src"])
        return urls

    def location(self) -> str:
        city_str = self.soup.find("p", class_="prev_city")
        location_str = self.soup.find("p", class_="prev_location")
        location_strings = []
        if location_str:
            location_str = location_str.find('span').text.replace("Location:", "")
            location_strings.append(location_str.strip())
        if city_str:
            city_str = city_str.find('span').string.replace("City:", "")
            location_strings.append(city_str.strip())
        
        return (" ").join(location_strings).strip()

    def ethnicity(self) -> str:
        return None

    def gender(self) -> str:
        return None

    def services(self) -> List:
        return None

    def website(self) -> str:
        return None

    def ad_text(self) -> str:
        # TODO: Think of better way to handle this overall
        dead_post = self.soup.find("div", id="deleted_post")
        if dead_post:
            return ""
        content = "\n".join(
            string
            for string in self.soup.find("div", class_="container").stripped_strings
        )
        return content.replace(u"\xa0", u" ")

    def ad_title(self) -> str:
        dead_post = self.soup.find("div", id="deleted_post")
        if dead_post:
            return ""
        title = self.soup.find("div", class_="post_preview_title")

        # Strip out the post time from the title text
        title_date = title.find("div", class_="post_preview_date_time")
        if title_date:
            title_date.decompose()

        title_text = " ".join(string for string in title.stripped_strings)
        return title_text

    def orientation(self) -> str:
        return None
