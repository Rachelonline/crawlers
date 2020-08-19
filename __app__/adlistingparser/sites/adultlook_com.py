from __app__.adlistingparser.sites.base_adlisting_parser import (
    BaseAdListingParser,
    AdListing,
)
from urllib.parse import urljoin

GENDER_MAPPING = {"Female": "female", "Transsexual": "trans", "Male": "male"}

SERVICE_MAPPING = {
    "Massage": "massage",
    "Body Rubs": "massage",
    "Domination": "bdsm",
    "Escort": "escort",
}


class AdultLook_com(BaseAdListingParser):

    # Going forward, this class should take a metadata/context that contains the domain.
    _domain = "https://www.adultlook.com"

    def ad_listings(self):
        links = [
            listing.get("href")
            for listing in self.soup.select("#results .grid-title a")
        ]
        links = filter(lambda x: x is not None, links)
        return [AdListing(self._get_full_url(link)) for link in links]

    def continuation_url(self):
        maybe_next_page = self.soup.select_one("[rel='next']")
        if maybe_next_page:
            return self._get_full_url(maybe_next_page.get("href"))

    def ad_listing_data(self) -> dict:
        metadata = {}
        # Use Breadcrumb to trace path
        breadcrumb = self.soup.find(class_="breadcrumb")
        if breadcrumb:
            breadcrumb_text = [item.text.strip() for item in breadcrumb.select("li")]
            _, country, state, city, service, *_ = breadcrumb_text

            metadata["location"] = ", ".join((country, state, city))

            if service:
                for key in SERVICE_MAPPING:
                    if key in service:
                        metadata["services"] = SERVICE_MAPPING[
                            key
                        ]  # found more specific service
                        break

                for key in GENDER_MAPPING:
                    if key in service:
                        metadata["gender"] = GENDER_MAPPING[key]

        return metadata

    def _get_full_url(self, url):
        return urljoin(self.__class__._domain, url)
