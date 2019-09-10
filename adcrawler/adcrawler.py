from datetime import datetime
import logging
from utils.network.network import get_url


def crawl_ad(message: dict) -> dict:
    parse_message = {}
    page = get_url(message["ad-url"])
    parse_message["ad-page"] = page.text
    parse_message["metadata"] = message["metadata"]
    parse_message["metadata"].update(
        {"ad-crawled": datetime.now().replace(microsecond=0).isoformat()}
    )
    logging.info("crawled ad: %s", message["ad-url"])

    return parse_message
