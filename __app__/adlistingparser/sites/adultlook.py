from __app__.adlistingparser.sites.base_adlisting_parser import BaseAdListingParser, AdListing
from urllib.parse import urljoin


class AdultLook(BaseAdListingParser):

    # Going forward, this class should take a metadata/context that contains the domain
    # within it.
    _domain = "https://www.adultlook.com"

    def ad_listings(self):
        listings = self.soup.select("#results > div > div:nth-child(2) > div:nth-child(1) > div")
        links = [listing.select_one("a") for listing in listings]
        links = filter(lambda x: x is not None, links)
        return [AdListing(self._get_full_url(link["href"])) for link in links if link.has_attr("href")]

    def continuation_url(self):
        maybe_next_page = self.soup.find(class_="next-page")
        if maybe_next_page:
            next_btn = maybe_next_page.select_one("a")
            return self._get_full_url(next_btn["href"])
        else:
            return ""

    def ad_listing_data(self) -> dict:
        # Use Breadcrumb to trace path
        breadcrumb = self.soup.find(class_="breadcrumb")

        breadcrumb_text = [item.text.strip() for item in breadcrumb.select("li")]
        _, country, state, city, service, *_ = breadcrumb_text

        metadata = {"country": country, "state": state, "city": city, "service": service}
        return metadata

    def _get_full_url(self, url):

        return urljoin(self.__class__._domain, url)


if __name__ == "__main__":
    import pathlib

    with open(pathlib.Path('../tests/test-html') / "20200621_adultlook_1.html") as f:
        data = {"ad-listing-page": f.read()}
        p = AdultLook(data)
        print(p.ad_listings())
        print(p.continuation_url())
        print(p.ad_listing_data())
