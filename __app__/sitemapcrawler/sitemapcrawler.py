import logging
from __app__.sitemapcrawler.sites.cityxguide_com import CityXGuide
from __app__.utils.metrics.metrics import get_client, enable_logging


SITE_MAP_CRAWLERS = {"cityxguide.com": CityXGuide}


def sitemap(message: dict) -> dict:
    azure_tc = get_client()
    logging.info(azure_tc)
    enable_logging()

    parse_message = {}
    site_map_crawler = SITE_MAP_CRAWLERS.get(message["domain"])
    if site_map_crawler is None:
        azure_tc.track_metric(
            "sitemap-crawl-error", 1, properties={"domain": message["domain"]}
        )

        logging.error("No site map crawler for %s", message["domain"])
        azure_tc.flush()
        return None

    site_map_crawler = site_map_crawler()
    parse_message["sitemapping-page"] = site_map_crawler.get_ad_listing_page()
    parse_message["domain"] = message["domain"]
    parse_message["metadata"] = message["metadata"]
    parse_message["metadata"].update(site_map_crawler.extra_metadata())
    azure_tc.track_metric("sitemap-crawl-success", 1, properties={"domain": message["domain"]})
    logging.info("completed sitemapping for %s", message["domain"])
    azure_tc.flush()
    return parse_message
