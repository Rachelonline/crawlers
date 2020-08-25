from __app__.adlistingparser.sites.base_adlisting_parser import (
    BaseAdListingParser,
    AdListing,
)
from urllib.parse import urljoin


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
        maybe_next_page = self.soup.select_one(".next-page")
        if maybe_next_page:
            return self._get_full_url(maybe_next_page.get("href"))

    def ad_listing_data(self) -> dict:
        # adlisting does not hold location or services, on per ad basis
        metadata = {
            "gender": "female"  # almost all ads are female; ad parser catches exceptions
        }

        return metadata

    def _get_full_url(self, url):
        return urljoin(self.__class__._domain, url)
