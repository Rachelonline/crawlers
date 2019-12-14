import pytest
import json
import os
from typing import List
from tests.fixtures.no_network import *
from __app__.adlistingparser.adlistingparser import AD_LISTING_PARSERS
from __app__.adlistingparser.sites.base_adlisting_parser import AdListing


TEST_DATA_LOCATION = "__app__/adlistingparser/tests/ad-listing-tests-data.json"
TEST_HTML_FOLDER = "__app__/adlistingparser/tests/test-data"


def id_func(item: dict) -> str:
    return item["html"]


def pytest_generate_tests(metafunc):
    if "test_case" in metafunc.fixturenames:
        with open(TEST_DATA_LOCATION, encoding="utf8") as test_data_f:
            test_cases = json.load(test_data_f)
            metafunc.parametrize("test_case", [i for i in test_cases], ids=id_func)


def build_ad_listings(ad_urls: List[dict]) -> AdListing:
    ad_listings = []
    for ad_url in ad_urls:
        ad_listings.append(AdListing(ad_url["ad-url"], ad_url.get("metadata", {})))
    return ad_listings

def test_site_map_parsers(test_case):
    with open(
        os.path.join(TEST_HTML_FOLDER, test_case["html"]), encoding="utf8"
    ) as html:
        page = html.read()

    test_case["ad-listing-page"] = page
    parser = AD_LISTING_PARSERS[test_case["domain"]]
    parser = parser(test_case)
    assert parser.ad_listings() == build_ad_listings(test_case["ad-urls"])
    assert parser.continuation_url() == test_case["next-url"]
    assert parser.ad_listing_data() == test_case["ad-listing-data"]
