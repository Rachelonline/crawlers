from datetime import datetime
from typing import List
import logging
from copy import deepcopy

from __app__.utils.table.ads import AdsTable
from __app__.adlistingparser.sites.base_adlisting_parser import AdListing
from __app__.adlistingparser.sites.cityxguide_com import CityXGuide_com
from __app__.adlistingparser.sites.escortdirectory import EscortDirectory
from __app__.adlistingparser.sites.vipgirlfriend_com import VIPGirlfriend_com
from __app__.adlistingparser.sites.megapersonals_eu import MegaPersonals_eu
from __app__.adlistingparser.sites.twobackpage_com import TwoBackpage_com
from __app__.adlistingparser.sites.gfemonkey_com import GfeMonkey_com
from __app__.adlistingparser.sites.onebackpage_com import OneBackPage_com
from __app__.adlistingparser.sites.bedpage_com import BedPage_com
from __app__.adlistingparser.sites.gfemonkey_com import GfeMonkey_com
from __app__.adlistingparser.sites.adultlook_com import AdultLook_com
from __app__.adlistingparser.sites.adultsearch_com import AdultSearch_com
from __app__.adlistingparser.sites.backpage_ly import BackPage_ly
from __app__.adlistingparser.sites.sumosear_ch import SumoSear_ch
from __app__.utils.metrics.metrics import get_client, enable_logging


AD_LISTING_PARSERS = {
    "cityxguide.com": CityXGuide_com,
    "vipgirlfriend.com": VIPGirlfriend_com,
    "escortdirectory.com": EscortDirectory,
    "megapersonals.eu": MegaPersonals_eu,
    "2backpage.com": TwoBackpage_com,
    "gfemonkey.com": GfeMonkey_com,
    "onebackpage.com": OneBackPage_com,
    "adultlook.com": AdultLook_com,
    "bedpage.com": BedPage_com,
    "adultsearch.com": AdultSearch_com,
    "backpage.ly": BackPage_ly,
    "sumosear.ch": SumoSear_ch
}


TABLE = AdsTable()
PERCENT_UNCRAWLED = 0.7
MAX_CRAWL_DEPTH = 10


def filter_uncrawled(ad_listings: List[AdListing]) -> List[AdListing]:
    uncrawled_ads = []
    for ad_listing in ad_listings:
        if not TABLE.is_crawled(ad_listing.ad_url):
            uncrawled_ads.append(ad_listing)
    return uncrawled_ads


def build_ad_listing_msgs(msg: dict, ad_listings: List[AdListing]) -> List[AdListing]:
    ad_listing_msgs = []
    for ad_listing in ad_listings:
        ad_msg = deepcopy(msg)
        ad_msg["ad-url"] = ad_listing.ad_url
        ad_msg["ad-id"] = ad_listing.hash()
        if ad_listing.metadata:
            if "ad-listing-data" in ad_msg:
                ad_msg["ad-listing-data"].update(ad_listing.metadata)
            else:
                ad_msg["ad-listing-data"] = ad_listing.metadata
        ad_listing_msgs.append(ad_msg)
    return ad_listing_msgs


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

    # Remove the ad-listing-page html
    message.pop("ad-listing-page", None)

    # Get metadata
    message["ad-listing-data"] = parser.ad_listing_data()

    ad_url_msgs = build_ad_listing_msgs(message, uncrawled_ads)

    # Check to see if we need to get the next ad listing page
    continuation_url = parser.continuation_url()
    continued_listing_msg = {}
    if ad_url_data and len(uncrawled_ads) / len(ad_url_data) >= PERCENT_UNCRAWLED:
        continued_listing_msg = build_cont_listing_msg(
            message, continuation_url, azure_tc
        )
    azure_tc.track_metric("ads-found", len(ad_url_data), properties={"domain": domain})
    azure_tc.track_metric(
        "new-ads-found", len(uncrawled_ads), properties={"domain": domain}
    )

    azure_tc.flush()

    return ad_url_msgs, continued_listing_msg
