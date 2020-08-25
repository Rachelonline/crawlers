import pytest
import json
import os
from glob import glob
from typing import List
from tests.fixtures.no_network import *
from __app__.sitemapparser.sitemapparser import parse_ad_listing_page

TEST_DATA_LOCATION = "__app__/sitemapparser/tests/test-data/*.json"
TEST_HTML_FOLDER = "__app__/sitemapparser/tests/test-html"


def id_func(item):
    return item["html"]


def case_data(case_loc: str) -> List:
    test_cases = []
    with open(case_loc, encoding="utf-8") as test_data_f:
        test_cases = json.load(test_data_f)

    return test_cases


def pytest_generate_tests(metafunc):
    if "test_case" in metafunc.fixturenames:
        test_cases = []
        for test_data_loc in glob(TEST_DATA_LOCATION):
            test_cases.extend(case_data(test_data_loc))
        metafunc.parametrize("test_case", [i for i in test_cases], ids=id_func)


def test_site_map_parsers(test_case):
    with open(
        os.path.join(TEST_HTML_FOLDER, test_case["html"]), encoding="utf8"
    ) as html:
        page = html.read()
    ad_listing_urls = parse_ad_listing_page(test_case["domain"], page)
    assert ad_listing_urls == test_case["ad-listing-urls"]
