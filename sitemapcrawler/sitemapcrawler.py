import logging
from sitemapcrawler.sites.cityxguide_com import CityXGuide


SITE_MAP_CRAWLERS = {"cityxguide.com": CityXGuide}

def sitemap(message: dict) -> dict:
    parse_message = {}
    site_map_crawler = SITE_MAP_CRAWLERS.get(message['domain'])
    if site_map_crawler is None:
        logging.error("No site map crawler for %s", message['domain'])
        return None
    site_map_crawler = site_map_crawler()
    parse_message['sitemapping_page'] = site_map_crawler.get_ad_listing_page()
    parse_message['metadata'] = message["metadata"]
    parse_message['metadata'].update(site_map_crawler.extra_metadata())
    logging.info("completed sitemapping for %s", message['domain'])

    return parse_message

