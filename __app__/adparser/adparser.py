from datetime import datetime
import logging
from copy import deepcopy
from __app__.utils.table.ads import AdsTable
from __app__.adparser.sites.cityxguide_com import CityXGuide
from __app__.adparser.sites.escortdirectory import EscortDirectory
from __app__.adparser.sites.megapersonals_eu import MegaPersonals
from __app__.adparser.sites.vipgirlfriend_com import VIPGirlfriend
from __app__.adparser.sites.twobackpage_com import TwoBackpage
from __app__.adparser.sites.onebackpage_com import OneBackPage_com
from __app__.adparser.sites.adultlook import AdultLookParser
from __app__.adparser.sites.bedpage_com import BedPage_com
from __app__.adparser.sites.gfemonkey_com import GfeMonkey

from __app__.utils.ads.adstore import get_ad_page
from __app__.utils.metrics.metrics import get_client, enable_logging

AD_PARSERS = {
    "cityxguide.com": CityXGuide,
    "cityxguide.net": CityXGuide,  # We can reuse this parser
    "vipgirlfriend.com": VIPGirlfriend,
    "escortdirectory.com": EscortDirectory,
    "megapersonals.eu": MegaPersonals,
    "2backpage.com": TwoBackpage,
    "onebackpage.com": OneBackPage_com,
    "adultlook.com": AdultLookParser,
    "bedpage.com": BedPage_com,
    "gfemonkey.com": GfeMonkey,
}

# {'ad-page-blob': 'https://picrawling.blob.core.windows.net/test-ads/2019/09/11/cityxguide.com/9675015e-858e-48d1-97c6-d7d3a8bcf74f', 'domain': 'cityxguide.com', 'metadata': {'domain': 'cityxguide.com', 'manual-job': True, 'ad-listing-crawled': '2019-09-10T17:04:02', 'ad-crawled': '2019-09-11T14:57:39'}##}
TABLE = AdsTable()


def parse_ads(domain, page):
    parser = AD_PARSERS.get(domain)
    if parser is None:
        logging.error("No ad parser for %s", domain)
        return {}
    parser = parser(page)
    return parser.ad_dict()


def build_image_url_msgs(msg: str, img_urls):
    img_url_msgs = []
    for url in img_urls:
        # TODO: disabling mp4s
        if url.endswith(".mp4"):
            continue
        img_url_msg = {}
        img_url_msg["image-url"] = url
        img_url_msg["domain"] = msg["domain"]
        img_url_msg["metadata"] = deepcopy(msg["metadata"])
        img_url_msgs.append(img_url_msg)
    return img_url_msgs


def build_ad_process_msg(msg: str, ad_data: dict) -> dict:
    ad_msg = deepcopy(msg)
    ad_msg["ad-data"] = ad_data
    return ad_msg


def parse_ad(message: dict) -> dict:
    azure_tc = get_client()
    enable_logging()

    page = get_ad_page(message["ad-page-blob"])
    domain = message["domain"]

    ad_data = parse_ads(domain, page)
    image_urls = ad_data["image-urls"]
    if not ad_data:
        azure_tc.track_metric(
            "ad-parse-failure", 1, properties={"domain": message["domain"]}
        )
        return {}, []

    parsed_on = datetime.utcnow().replace(microsecond=0)
    message["metadata"].update({"ad-parsed": parsed_on.isoformat()})
    TABLE.mark_parsed(message["ad-url"], message["metadata"], image_urls)

    ad_process_msg = build_ad_process_msg(message, ad_data)
    image_url_msgs = build_image_url_msgs(message, image_urls)

    azure_tc.track_metric(
        "ad-parse-success", 1, properties={"domain": message["domain"]}
    )
    azure_tc.track_metric(
        "images-found", len(image_urls), properties={"domain": message["domain"]}
    )

    azure_tc.flush()
    return ad_process_msg, image_url_msgs
