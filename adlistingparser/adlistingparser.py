from datetime import datetime
from typing import List
import logging
from copy import deepcopy
from utils.table.ads import AdsTable
from sitemapparser.sites.cityxguide_com import cityxguide_com

AD_LISTING_PARSERS = {"cityxguide.com": None}


TABLE = AdsTable()
PERCENT_UNCRAWLED = 0.7


def parse_ad_listings(domain, page):
    parser = AD_LISTING_PARSERS.get(domain)
    if parser is None:
        logging.error("No ad listing parser for %s", domain)
        return [], []
    ad_urls, continuation_urls = parser(page)
    return ad_urls, continuation_urls


def filter_uncrawled(ad_urls: List[str]) -> List[str]:
    uncrawled_ads = []
    for ad_url in ad_urls:
        if not TABLE.is_crawled(ad_url):
            uncrawled_ads.append(ad_url)
    return uncrawled_ads


def build_ad_url_msgs(msg: dict, ad_urls: List[str]) -> List[dict]:
    ad_url_msgs = []
    for url in ad_urls:
        ad_msg = {}
        ad_msg["domain"] = msg["domain"]
        ad_msg["ad-url"] = url
        ad_msg["metadata"] = deepcopy(msg["metadata"])
        ad_url_msgs.append(ad_msg)
    return ad_url_msgs


def build_cont_listing_msgs(msg: dict, next_urls: List[str]) -> List[dict]:
    continued_listing_msgs = []
    crawl_depth = msg["metadata"].get("crawl-depth", 0)
    logging.info(
        "not enough ads crawled, enqueing next ad listing url for %s, depth %s",
        msg["domain"],
        crawl_depth,
    )
    for next_url in next_urls:
        next_listing_msg = {}
        next_listing_msg["domain"] = msg["domain"]
        next_listing_msg["url"] = next_url
        next_listing_msg["metadata"] = deepcopy(msg["metadata"])
        next_listing_msg["metadata"]["crawl-depth"] = crawl_depth + 1
        continued_listing_msgs.append(next_listing_msg)
    return continued_listing_msgs


def parse_ad_listing(message: dict) -> dict:
    page = message["ad-listing-page"]
    domain = message["domain"]

    ad_urls, continuation_urls = parse_ad_listings(domain, page)
    logging.info("Found %s ads on %s", len(ad_urls), domain)
    logging.info("Found %s continuation urls on %s", len(continuation_urls), domain)

    # Perf improvement: make this parallel
    uncrawled_ads = filter_uncrawled(ad_urls)
    logging.info(
        "%s/%s ads are uncrawled on %s", len(uncrawled_ads), len(ad_urls), domain
    )
    ad_url_msgs = build_ad_url_msgs(message, uncrawled_ads)

    # Check to see if we need to get the next ad listing page
    continued_listing_msgs = []
    if len(uncrawled_ads) / len(ad_urls) >= PERCENT_UNCRAWLED:
        continued_listing_msgs = build_cont_listing_msgs(message, continuation_urls)

    return ad_url_msgs, continued_listing_msgs
