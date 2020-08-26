import pytest
import json
import os
from glob import glob
from typing import List
from tests.fixtures.no_network import *
from __app__.adlistingparser.adlistingparser import AD_LISTING_PARSERS
from __app__.adlistingparser.sites.base_adlisting_parser import AdListing


TEST_DATA_LOCATION = "__app__/adlistingparser/tests/test-data/*.json"
TEST_HTML_FOLDER = "__app__/adlistingparser/tests/test-html"


def id_func(item: dict) -> str:
    return item["html"]


def case_data(case_loc: str) -> List:
    test_cases = []
    with open(case_loc, encoding="utf8") as test_data_f:
        test_cases = json.load(test_data_f)

    return test_cases


def pytest_generate_tests(metafunc):
    if "test_case" in metafunc.fixturenames:
        test_cases = []
        for test_data_loc in glob(TEST_DATA_LOCATION):
            test_cases.extend(case_data(test_data_loc))
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
    print("Parser ad listings")
    for listing in parser.ad_listings():
        print(str(listing))
    print("\n\ntest case listings")
    for listing in build_ad_listngs(test_case["ad-urls"]):
        print(str(listing))
    assert parser.ad_listings() == build_ad_listings(test_case["ad-urls"])
    if "next-url" in test_case.keys():  # if last page, next-url will not exist
        assert parser.continuation_url() == test_case["next-url"]

    assert parser.ad_listing_data() == test_case["ad-listing-data"]
