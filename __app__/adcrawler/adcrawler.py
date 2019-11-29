from datetime import datetime
import logging
from __app__.utils.network.network import get_url
from __app__.utils.table.ads import AdsTable
from __app__.utils.ads.adstore import save_ad_page
from __app__.utils.metrics.metrics import get_client, enable_logging
from __app__.utils.throttle.throttle import check_throttle

TABLE = AdsTable()


def crawl_ad(message: dict) -> dict:
    azure_tc = get_client()
    enable_logging()

    ad_url = message["ad-url"]
    domain = message["domain"]
    logging.info("starting crawl: %s", ad_url)
    # We've already crawled this page
    if TABLE.is_crawled(ad_url):
        azure_tc.track_metric(
            "ad-already-crawled", 1, properties={"domain": message["domain"]}
        )
        logging.info("already-crawled: %s", ad_url)
        azure_tc.flush()
        return None
    logging.info("checking throttle: %s", ad_url)
    check_throttle(ad_url, azure_tc=azure_tc)
    logging.info("getting page: %s", ad_url)
    page = get_url(ad_url)
    logging.info("saving blob: %s", ad_url)
    crawled_on = datetime.utcnow().replace(microsecond=0)
    uri = save_ad_page(page, crawled_on, domain)

    message["ad-page-blob"] = uri
    message["metadata"].update({"ad-crawled": crawled_on.isoformat()})

    logging.info("crawled ad: %s", ad_url)
    TABLE.mark_crawled(ad_url, uri, message["metadata"])

    azure_tc.track_metric(
        "ad-crawl-success", 1, properties={"domain": message["domain"]}
    )
    azure_tc.flush()

    return message
