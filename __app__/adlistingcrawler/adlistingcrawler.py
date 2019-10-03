from datetime import datetime
import logging
from __app__.utils.network.network import get_url


def crawl_ad_listing(message: dict) -> dict:
    parse_message = {}
    page = get_url(message["ad-listing-url"])
    parse_message["ad-listing-page"] = page.text
    parse_message["domain"] = message["domain"]
    parse_message["metadata"] = message["metadata"]
    parse_message["metadata"].update(
        {"ad-listing-crawled": datetime.now().replace(microsecond=0).isoformat()}
    )
    logging.info("crawled ad listing url: %s", message["ad-listing-url"])

    return parse_message
