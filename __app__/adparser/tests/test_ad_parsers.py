import pytest
import json
import os
from operator import attrgetter
from tests.fixtures.no_network import *
from __app__.adparser.adparser import parse_ads


TEST_DATA_LOCATION = "__app__/adparser/tests/ad-test-data.json"
TEST_HTML_FOLDER = "__app__/adparser/tests/test-data"


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
    ad_data = parse_ads(test_case["domain"], page)
    assert ad_data == test_case["ad-data"]
