from urllib.parse import urljoin
from typing import List
from __app__.adparser.sites.base_ad_parser import BaseAdParser


class VIPGirlfriend(BaseAdParser):
    gender_lookup = {"female-escort": "female", "male-escort": "male"}

    def primary_phone_number(self) -> str:
        phone_div = self.soup.find("li", class_="lp-listing-phone")
        if phone_div:
          return next(phone_div.stripped_strings)

    def phone_numbers(self) -> List:
        phone_numbers_found = []
        prim_phone_number = self.primary_phone_number()
        if prim_phone_number:
            phone_numbers_found.append(prim_phone_number)
        matches = self.phone_re.findall(self.ad_text())
        phone_numbers_found.extend(["".join(match) for match in matches])
        return phone_numbers_found

    def date_posted(self) -> str:
        return None

    def name(self) -> str:
        return self.soup.find("h1").string.strip()

    def primary_email(self) -> str:
        return None

    def emails(self) -> List:
        emails_found = []
        matches = self.email_re.findall(self.ad_text())
        emails_found.extend(["".join(match) for match in matches])
        return emails_found

    def social(self) -> List:
        social = []
        social_div = self.soup.find("div", class_="widget-social")
        if social_div:
          links = social_div.find_all("a", href=True) or []
          for link in links:
            social.append(link["href"])
        return social

    def age(self) -> str:
        return None

    def image_urls(self) -> List:
        urls = []
        image_div = self.soup.find("div", class_="listing-slide")
        images = image_div("img", src=True) or []
        for image in images:
            urls.append(urljoin("http:", image["src"]))
        return urls

    def location(self) -> str:
        location_div = self.soup.find("li", class_="lp-details-address")
        if location_div:
            return next(location_div.stripped_strings)

    def ethnicity(self) -> str:
        return None

    def gender(self) -> str:
        gender = None
        categories = self.soup.find("ul", class_="features")
        if categories:
          link = categories.find("a").get("href")
          gender = self.gender_lookup.get(link.split("/")[-2], "unknown")
        return gender

    def services(self) -> List:
        services = None
        categories = self.soup.find("ul", class_="breadcrumbs").find_all("a")
        if categories:
          services = []
        for category in categories:
          if category.text != "Home":
            services.append(category.text)
        return services

    def website(self) -> str:
        website_span = self.soup.find("li", class_="lp-user-web")
        if website_span:
          return next(website_span.stripped_strings)

    def ad_text(self) -> str:
        content = "\n".join(
            string
            for string in self.soup.find("div", class_="post-detail-content").stripped_strings
        )
        if content:
            return content

    def ad_title(self) -> str:
        content = ""
        subheadings = self.soup.find("h1").next_siblings
        for subheading in subheadings:
          if type(subheading).__name__ == 'Tag':
            content += subheading.text
          else:
            content += subheading.strip()
        if content:
            content = content.rjust(len(content)+1)
        return self.name() + content