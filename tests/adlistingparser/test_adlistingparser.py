import pytest
from unittest.mock import MagicMock
from tests.fixtures.no_network import *
from adlistingparser.adlistingparser import (
    AD_LISTING_PARSERS,
    parse_ad_listings,
    filter_uncrawled,
    build_ad_url_msgs,
    build_cont_listing_msgs,
    parse_ad_listing,
)


def fake_parser(page):
    return ["ad-url1", "ad-url2"], ["cont-url"]


def not_found_parser(page):
    return [], []


@pytest.fixture
def parsers(monkeypatch):
    monkeypatch.setitem(AD_LISTING_PARSERS, "fake-parser", fake_parser)
    monkeypatch.setitem(AD_LISTING_PARSERS, "no-urls-found-parser", not_found_parser)


def test_parse_ad_listing_page(parsers):
    assert parse_ad_listings("fake-parser", "<html>") == (
        ["ad-url1", "ad-url2"],
        ["cont-url"],
    )
    assert parse_ad_listings("no-urls-found-parser", "<html>") == ([], [])
    assert parse_ad_listings("no domain", "<html>") == ([], [])


def test_filter_uncrawled(monkeypatch):
    mock_table = MagicMock()
    monkeypatch.setattr("adlistingparser.adlistingparser.TABLE", mock_table)

    mock_table.is_crawled.side_effect = [False, True, False]
    assert ["ad-url1", "ad-url3"] == filter_uncrawled(["ad-url1", "ad-url2", "ad-url3"])


def test_build_ad_url_msgs():
    test_msg = {"domain": "test", "metadata": {"meta": "data"}}
    urls = ["ad-url1", "ad-url3"]

    expected = [
        {"domain": "test", "metadata": {"meta": "data"}, "ad-url": "ad-url1"},
        {"domain": "test", "metadata": {"meta": "data"}, "ad-url": "ad-url3"},
    ]
    assert build_ad_url_msgs(test_msg, urls) == expected


def test_build_cont_listing_msgs():
    test_msg = {"domain": "test", "metadata": {"meta": "data"}}
    urls = ["next-url1", "next-url3"]

    expected = [
        {
            "domain": "test",
            "metadata": {"meta": "data", "crawl-depth": 1},
            "url": "next-url1",
        },
        {
            "domain": "test",
            "metadata": {"meta": "data", "crawl-depth": 1},
            "url": "next-url3",
        },
    ]
    assert build_cont_listing_msgs(test_msg, urls) == expected

    test_msg = {"domain": "test", "metadata": {"meta": "data", "crawl-depth": 1}}
    urls = ["next-url4"]
    expected = [
        {
            "domain": "test",
            "metadata": {"meta": "data", "crawl-depth": 2},
            "url": "next-url4",
        }
    ]
    assert build_cont_listing_msgs(test_msg, urls) == expected

    # Beyond max crawl depth
    test_msg = {"domain": "test", "metadata": {"meta": "data", "crawl-depth": 10}}
    urls = ["next-url4"]
    expected = []
    assert build_cont_listing_msgs(test_msg, urls) == expected



def test_parse_ad_listing(monkeypatch):
    msg = {"ad-listing-page": "<html>", "domain": "test-domain"}

    parse_mock = MagicMock()
    parse_mock.return_value = (
        ["ad-url1", "ad-url2", "ad-url3", "ad-url4"],
        ["next-url"],
    )
    monkeypatch.setattr("adlistingparser.adlistingparser.parse_ad_listings", parse_mock)

    uncrawled_mock = MagicMock()
    monkeypatch.setattr(
        "adlistingparser.adlistingparser.filter_uncrawled", uncrawled_mock
    )

    ad_msg_mock = MagicMock()
    ad_msg_mock.return_value = ["ad-mgs"]
    monkeypatch.setattr(
        "adlistingparser.adlistingparser.build_ad_url_msgs", ad_msg_mock
    )

    cont_msg_mock = MagicMock()
    cont_msg_mock.return_value = ["cont-mgs"]
    monkeypatch.setattr(
        "adlistingparser.adlistingparser.build_cont_listing_msgs", cont_msg_mock
    )

    # no ads have been crawled - be sure we're going to keep crawling
    uncrawled_mock.return_value = ["ad-url1", "ad-url2", "ad-url3", "ad-url4"]
    assert parse_ad_listing(msg) == (["ad-mgs"], ["cont-mgs"])

    # not enough ads have been crawled - be sure we're going to keep crawling
    uncrawled_mock.return_value = ["ad-url1", "ad-url2", "ad-url3"]
    assert parse_ad_listing(msg) == (["ad-mgs"], ["cont-mgs"])

    # enough ads have been crawled - we don't want to continue
    uncrawled_mock.return_value = ["ad-url1", "ad-url3"]
    assert parse_ad_listing(msg) == (["ad-mgs"], [])
