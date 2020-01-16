import pytest
from unittest.mock import MagicMock
from tests.fixtures.no_network import *
from __app__.adlistingparser.adlistingparser import (
    AD_LISTING_PARSERS,
    filter_uncrawled,
    build_cont_listing_msg,
    build_ad_listing_msgs,
    parse_ad_listing,
)
from __app__.adlistingparser.sites.base_adlisting_parser import AdListing


def test_filter_uncrawled(monkeypatch):
    mock_table = MagicMock()
    monkeypatch.setattr("__app__.adlistingparser.adlistingparser.TABLE", mock_table)

    mock_table.is_crawled.side_effect = [False, True, False]
    assert [AdListing("ad-url1"), AdListing("ad-url3")] == filter_uncrawled(
        [AdListing("ad-url1"), AdListing("ad-url2"), AdListing("ad-url3")]
    )


def test_build_ad_listing_msgs():
    test_msg = {"domain": "test", "metadata": {"meta": "data"}}
    urls = [AdListing("ad-url1"), AdListing("ad-url3", {"extra": "metadata"})]

    expected = [
        {"domain": "test", "metadata": {"meta": "data"}, "ad-url": "ad-url1"},
        {
            "domain": "test",
            "metadata": {"meta": "data"},
            "ad-listing-data": {"extra": "metadata"},
            "ad-url": "ad-url3",
        },
    ]
    assert build_ad_listing_msgs(test_msg, urls) == expected


def test_build_cont_listing_msgs():
    test_msg = {"domain": "test", "metadata": {"meta": "data"}}
    urls = "next-url1"

    expected = {
        "domain": "test",
        "metadata": {"meta": "data", "crawl-depth": 1},
        "ad-listing-url": "next-url1",
    }
    assert build_cont_listing_msg(test_msg, urls, MagicMock()) == expected

    # Beyond max crawl depth
    test_msg = {"domain": "test", "metadata": {"meta": "data", "crawl-depth": 10}}
    urls = "next-url4"
    expected = {}
    assert build_cont_listing_msg(test_msg, urls, MagicMock()) == expected


@pytest.fixture
def fake_parser(monkeypatch):
    mock_parser = MagicMock()
    mock_parser.return_value.ad_listings.return_value = [
        "ad-url1",
        "ad-url2",
        "ad-url3",
        "ad-url4",
    ]
    mock_parser.continuation_url.return_value = "next-url"
    monkeypatch.setitem(AD_LISTING_PARSERS, "test-domain", mock_parser)
    return mock_parser


def test_parse_ad_listing(monkeypatch, fake_parser):
    msg = {"ad-listing-page": "<html>", "domain": "test-domain"}

    uncrawled_mock = MagicMock()
    monkeypatch.setattr(
        "__app__.adlistingparser.adlistingparser.filter_uncrawled", uncrawled_mock
    )

    ad_msg_mock = MagicMock()
    ad_msg_mock.return_value = ["ad-mgs"]
    monkeypatch.setattr(
        "__app__.adlistingparser.adlistingparser.build_ad_listing_msgs", ad_msg_mock
    )

    cont_msg_mock = MagicMock()
    cont_msg_mock.return_value = {"cont-mgs": "test"}
    monkeypatch.setattr(
        "__app__.adlistingparser.adlistingparser.build_cont_listing_msg", cont_msg_mock
    )

    # no ads have been crawled - be sure we're going to keep crawling
    uncrawled_mock.return_value = ["ad-url1", "ad-url2", "ad-url3", "ad-url4"]
    assert parse_ad_listing(msg) == (["ad-mgs"], {"cont-mgs": "test"})

    # not enough ads have been crawled - be sure we're going to keep crawling
    uncrawled_mock.return_value = ["ad-url1", "ad-url2", "ad-url3"]
    assert parse_ad_listing(msg) == (["ad-mgs"], {"cont-mgs": "test"})

    # enough ads have been crawled - we don't want to continue
    uncrawled_mock.return_value = ["ad-url1", "ad-url3"]
    assert parse_ad_listing(msg) == (["ad-mgs"], {})
