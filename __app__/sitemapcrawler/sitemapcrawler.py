import logging
from datetime import datetime
from __app__.utils.metrics.metrics import get_client, enable_logging
from __app__.utils.network.network import get_url
from __app__.utils.throttle.throttle import check_throttle

SITEMAP_URL = {
    "capleasures.com": "https://capleasures.com",
    "megapersonals.eu": "https://megapersonals.eu",
    "escortdirectory.com": "https://www.escortdirectory.com",
    "gfemonkey.com": "https://www.gfemonkey.com",
    "adultsearch.com": "https://www.adultsearch.com",
    "bedpage.com": "https://www.bedpage.com/",
    "adultlook.com": "https://www.adultlook.com/",
    # "cityxguide.com": "https://cityxguide.com", # Disabled using stop_crawling_domain.py 20200630
    # "cityxguide.net": "https://cityxguide.net" # Disabled using stop_crawling_domain.py 20200630
    # "onebackpage.com": "https://onebackpage.com" # Disabled using stop_crawling_domain.py 20200615
    # "vipgirlfriend.com": "https://vipgirlfriend.com",  # Disabled using stop_crawling_domain.py20191209
    # "2backpage.com": "https://2backpage.com", # Disabled using stop_crawling_domain.py 20201022
}


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
        {"site-map": datetime.utcnow().replace(microsecond=0).isoformat()}
    )

    azure_tc.track_metric("sitemap-crawl-success", 1, properties={"domain": domain})
    logging.info("completed sitemapping for %s", domain)
    azure_tc.flush()

    return parse_message
