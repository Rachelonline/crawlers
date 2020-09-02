from __app__.adlistingparser.sites.base_adlisting_parser import (
    BaseAdListingParser,
    AdListing,
)
from urllib.parse import urljoin

external_ad_url = (
    "/ad?go"  # sponsored link follows convention of https://domain/ad?go=<integer>
)


class AdultSearch_com(BaseAdListingParser):
    def ad_listings(self):
        links = [listing.get("href") for listing in self.soup.select(".card-view a")]
        links = filter(lambda x: x is not None and external_ad_url not in x, links)

        return [AdListing(link) for link in links]

    def continuation_url(self):
        maybe_next_page = self.soup.select_one(".next-arrow")
        if maybe_next_page:
            return maybe_next_page.get("href")  # contains full url + domain

    def ad_listing_data(self) -> dict:
        # adlisting does not hold location or services, on per ad basis
        metadata = {
            "gender": "female"  # almost all ads are female; ad parser catches exceptions
        }

        return metadata
