from datetime import datetime
import logging
from utils.network.network import get_url
from utils.table.ads import AdsTable
from utils.ads.adstore import save_ad_page

TABLE = AdsTable()


def crawl_ad(message: dict) -> dict:
    ad_url = message["ad-url"]
    domain = message["domain"]
    # We've already crawled this page
    if TABLE.is_crawled(ad_url):
        return None

    parse_message = {}
    page = get_url(ad_url)
    crawled_on = datetime.now().replace(microsecond=0)
    uri = save_ad_page(page, crawled_on, domain)

    parse_message["ad-page-blob"] = uri
    parse_message["domain"] = domain
    parse_message["metadata"] = message["metadata"]
    parse_message["metadata"].update({"ad-crawled": crawled_on.isoformat()})

    logging.info("crawled ad: %s", ad_url)
    TABLE.mark_crawled(ad_url, uri, parse_message["metadata"])

    return parse_message
