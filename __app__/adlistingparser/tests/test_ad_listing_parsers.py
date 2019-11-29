import pytest
import json
import os
from tests.fixtures.no_network import *
from __app__.adlistingparser.adlistingparser import AD_LISTING_PARSERS


TEST_DATA_LOCATION = "__app__/adlistingparser/tests/ad-listing-tests-data.json"
TEST_HTML_FOLDER = "__app__/adlistingparser/tests/test-data"


def id_func(item):
    return item["html"]


def pytest_generate_tests(metafunc):
    if "test_case" in metafunc.fixturenames:
        with open(TEST_DATA_LOCATION, encoding="utf8") as test_data_f:
            test_cases = json.load(test_data_f)
            metafunc.parametrize("test_case", [i for i in test_cases], ids=id_func)


def test_site_map_parsers(test_case):
    with open(
        os.path.join(TEST_HTML_FOLDER, test_case["html"]), encoding="utf8"
    ) as html:
        page = html.read()

    test_case["ad-listing-page"] = page
    parser = AD_LISTING_PARSERS[test_case["domain"]]
    parser = parser(test_case)
    assert parser.ad_listings() == test_case["ad-urls"]
    assert parser.continuation_url() == test_case["next-url"]
    assert parser.ad_listing_data() == test_case["ad-listing-data"]
