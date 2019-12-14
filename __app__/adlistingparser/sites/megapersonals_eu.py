from urllib.parse import urljoin
from bs4 import BeautifulSoup
from __app__.adlistingparser.sites.base_adlisting_parser import BaseAdListingParser, AdListing


GENDER_IMG_MAP = {
    "/resources/img/listtitle_wsm.png": "female",
    "/resources/img/listtitle_msm.png": "male",
    "/resources/img/listtitle_trans.png": "trans",
}


class MegaPersonals_eu(BaseAdListingParser):
    def ad_listings(self):
        ad_listings = []

        posts = self.soup.find_all("div", class_="listadd")

        for post in posts:
            link = post.find("a", class_="listtitle")
            url = f"https://megapersonals.eu{link.get('href')}"

            prev_date = post.find_previous_sibling("div", class_="briefdate")
            prev_date = prev_date.text.strip()

            ad_listings.append(AdListing(url, metadata={"ad-date-posted": prev_date}))

        return ad_listings

    def continuation_url(self):
        next_div = self.soup.find("div", id="paginationNext")
        if next_div:
            link = next_div.parent
            return f"https://megapersonals.eu{link.get('href')}"

    def ad_listing_data(self) -> dict:
        metadata = {}

        # Find location
        location = self.soup.find("span", class_="mpcityname")
        if location:
            metadata["location"] = location.text.strip()

        # Gender
        # We find the gender by looking at the image
        # If we passed down metadata from the sitemapping we could skip this step
        top_image = self.soup.find("img", class_="listtitleimg")
        if top_image:
            metadata["gender"] = GENDER_IMG_MAP.get(top_image.get("src"), "unknown")

        return metadata
