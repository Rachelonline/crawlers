import pytest
import json
import os
from tests.fixtures.no_network import *
from sitemapparser.sitemapparser import parse_ad_listing_page


TEST_DATA_LOCATION = "sitemapparser/tests/site-map-test-data.json"
TEST_HTML_FOLDER = "sitemapparser/tests/test-data"


def test_site_map_parsers(monkeypatch):
    # TODO: Parameterize this bad boy
    with open(TEST_DATA_LOCATION) as test_data_f:
        test_cases = json.load(test_data_f)

    for test_case in test_cases:
        with open(os.path.join(TEST_HTML_FOLDER, test_case["html"])) as html:
            page = html.read()
        ad_listing_urls = parse_ad_listing_page(test_case["domain"], page)
        assert ad_listing_urls == test_case["ad-listing-urls"]
