from __app__.adlistingparser.sites.base_adlisting_parser import BaseAdListingParser, AdListing

class AdultLook(BaseAdListingParser):
    def ad_listings(self):
        listings = self.soup.select("#results > div > div:nth-child(2) > div:nth-child(1) > div")
        return [AdListing(listing.select_one("a")["href"]) for listing in listings]

    def continuation_url(self):
        # There is no pagination; the "view more" button on this site
        # takes you to another region listing page
        next_btn = self.soup.find(class_="next_page").select("a")
        return next_btn["href"]

    def ad_listing_data(self) -> dict:
        # Use Breadcrumb to trace path
        breadcrumb = self.soup.find(class_="breadcrumb")

        breadcrumb_text = [item.text.strip() for item in breadcrumb.select("li")]
        _, country, state, city, service, *_ = breadcrumb_text

        metadata = {"country": country, "state": state, "city": city, "service": service}
        return metadata
