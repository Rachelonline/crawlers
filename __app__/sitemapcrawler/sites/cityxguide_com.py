from __app__.utils.network.network import get_url
from datetime import datetime
from __app__.sitemapcrawler.sites.base_site_mapper import SiteMapper


class CityXGuide(SiteMapper):
    AD_LISTING_URL = "https://cityxguide.com"

    def get_ad_listing_page(self):
        page = get_url(self.AD_LISTING_URL)
        return page.text

    def extra_metadata(self):
        return {"site-map": datetime.now().replace(microsecond=0).isoformat()}
