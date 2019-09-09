import logging
from sitemapper.sites.cityxguide_com import CityXGuide


SITE_MAPPING = {"cityxguide.com": CityXGuide}

def sitemap(message: dict) -> dict:
    parse_message = {}
    site_mapper = SITE_MAPPING.get(message['domain'])
    if site_mapper is None:
        logging.error("No site map crawler for %s", message['domain'])
        return None
    site_mapper = site_mapper()
    parse_message['sitemapping_page'] = site_mapper.get_ad_listing_page()
    parse_message['metadata'] = message["metadata"]
    parse_message['metadata'].update(site_mapper.extra_metadata())
    logging.info("completed sitemapping for %s", message['domain'])

    return parse_message

