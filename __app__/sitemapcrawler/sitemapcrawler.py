import logging
from datetime import datetime
from __app__.utils.metrics.metrics import get_client, enable_logging
from __app__.utils.network.network import get_url
from __app__.utils.throttle.throttle import check_throttle

SITEMAP_URL = {"cityxguide.com": "https://cityxguide.com"}


def get_sitemap_page(sitemap_url):
    return get_url(sitemap_url)


def sitemap(message: dict) -> dict:
    azure_tc = get_client()
    enable_logging()

    domain = message["domain"]
    sitemap_url = SITEMAP_URL.get(domain)
    if sitemap_url is None:
        azure_tc.track_metric("sitemap-crawl-error", 1, properties={"domain": domain})
        logging.error("No site map crawler for %s", domain)
        azure_tc.flush()
        return None

    check_throttle(sitemap_url, azure_tc=azure_tc)
    parse_message = {}
    parse_message["sitemapping-page"] = get_sitemap_page(sitemap_url)
    parse_message["domain"] = message["domain"]
    parse_message["metadata"] = message["metadata"]
    parse_message["metadata"].update(
        {"site-map": datetime.now().replace(microsecond=0).isoformat()}
    )

    azure_tc.track_metric("sitemap-crawl-success", 1, properties={"domain": domain})
    logging.info("completed sitemapping for %s", domain)
    azure_tc.flush()

    return parse_message
