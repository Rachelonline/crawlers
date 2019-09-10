import pytest
import json
import os
from tests.fixtures.no_network import *
from adlistingparser.adlistingparser import parse_ad_listings


TEST_DATA_LOCATION = "adlistingparser/tests/ad-listing-tests-data.json"
TEST_HTML_FOLDER = "adlistingparser/tests/test-data"


def test_site_map_parsers(monkeypatch):
    # TODO: Parameterize this bad boy
    with open(TEST_DATA_LOCATION) as test_data_f:
        test_cases = json.load(test_data_f)

    for test_case in test_cases:
        with open(os.path.join(TEST_HTML_FOLDER, test_case["html"])) as html:
            page = html.read()
        ad_listing_urls, next_urls = parse_ad_listings(test_case["domain"], page)
        assert ad_listing_urls == test_case["ad-urls"]
        assert next_urls == test_case["next-urls"]
