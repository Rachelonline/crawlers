from datetime import datetime
import logging
from __app__.utils.network.network import get_url
from __app__.utils.metrics.metrics import get_client, enable_logging
from __app__.utils.throttle.throttle import check_throttle


def crawl_ad_listing(message: dict) -> dict:
    azure_tc = get_client()
    enable_logging()

    ad_listing_url = message["ad-listing-url"]
    check_throttle(ad_listing_url, azure_tc=azure_tc)
    page = get_url(ad_listing_url)
    message["ad-listing-page"] = page.text
    message["domain"] = message["domain"]
    message["metadata"].update(
        {"ad-listing-crawled": datetime.now().replace(microsecond=0).isoformat()}
    )
    logging.info("crawled ad listing url: %s", message["ad-listing-url"])
    azure_tc.track_metric(
        "adlisting-crawl-success", 1, properties={"domain": message["domain"]}
    )
    azure_tc.flush()

    return message
