from datetime import datetime
from typing import List
import logging
from copy import deepcopy
from __app__.utils.table.ads import AdsTable
from __app__.adlistingparser.sites.cityxguide_com import CityXGuide_com
from __app__.adlistingparser.sites.escortdirectory import EscortDirectory
from __app__.adlistingparser.sites.vipgirlfriend_com import VIPGirlfriend_com
from __app__.utils.metrics.metrics import get_client, enable_logging

AD_LISTING_PARSERS = {
    "cityxguide.com": CityXGuide_com,
    "vipgirlfriend.com": VIPGirlfriend_com,
    "escortdirectory.com": EscortDirectory,
}


TABLE = AdsTable()
PERCENT_UNCRAWLED = 0.7
MAX_CRAWL_DEPTH = 10


def filter_uncrawled(ad_urls: List[str]) -> List[str]:
    uncrawled_ads = []
    for ad_url in ad_urls:
        if not TABLE.is_crawled(ad_url):
            uncrawled_ads.append(ad_url)
    return uncrawled_ads


def build_ad_url_msgs(msg: dict, ad_urls: List[str]) -> List[dict]:
    ad_url_msgs = []
    for url in ad_urls:
        ad_msg = deepcopy(msg)
        ad_msg["ad-url"] = url
        ad_url_msgs.append(ad_msg)
    return ad_url_msgs


def build_cont_listing_msg(message: dict, continuation_url: str, azure_tc) -> dict:
    if not continuation_url:
        return None
    crawl_depth = message["metadata"].get("crawl-depth", 0)
    domain = message["domain"]
    azure_tc.track_metric("crawl-depth", crawl_depth, properties={"domain": domain})

    if crawl_depth >= MAX_CRAWL_DEPTH:
        azure_tc.track_metric("crawl-depth-max", 1, properties={"domain": domain})
        return {}
    continuation_msg = deepcopy(message)
    continuation_msg["ad-listing-url"] = continuation_url
    continuation_msg["metadata"]["crawl-depth"] = crawl_depth + 1
    azure_tc.track_metric("continuation-urls", 1, properties={"domain": domain})
    return continuation_msg


def parse_ad_listing(message: dict) -> dict:
    azure_tc = get_client()
    enable_logging()

    domain = message["domain"]
    parser = AD_LISTING_PARSERS.get(domain)
    if parser is None:
        logging.error("No ad listing parser for %s", domain)
        return [], {}
    parser = parser(message)
    ad_url_data = parser.ad_listings()
    # Perf improvement: make filtering parallel
    uncrawled_ads = filter_uncrawled(ad_url_data)
    azure_tc.track_metric("ads-found", len(ad_url_data), properties={"domain": domain})
    azure_tc.track_metric(
        "new-ads-found", len(uncrawled_ads), properties={"domain": domain}
    )

    # Remove the ad-listing-page html
    message.pop("ad-listing-page", None)

    # Get metadata
    message["ad-listing-data"] = parser.ad_listing_data()

    ad_url_msgs = build_ad_url_msgs(message, uncrawled_ads)

    # Check to see if we need to get the next ad listing page
    continuation_url = parser.continuation_url()
    continued_listing_msg = {}
    if ad_url_data and len(uncrawled_ads) / len(ad_url_data) >= PERCENT_UNCRAWLED:
        continued_listing_msg = build_cont_listing_msg(
            message, continuation_url, azure_tc
        )

    azure_tc.flush()

    return ad_url_msgs, continued_listing_msg
