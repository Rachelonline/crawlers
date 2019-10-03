import pytest
from unittest.mock import MagicMock
from tests.fixtures.no_network import *
from __app__.sitemapparser.sitemapparser import (
    SITE_PARSERS,
    parse_ad_listing_page,
    parse_sitemap,
)


def fake_parser(page):
    return ["test-url1", "test-url2"]


def not_found_parser(page):
    return []


@pytest.fixture
def parsers(monkeypatch):
    monkeypatch.setitem(SITE_PARSERS, "fake-parser", fake_parser)
    monkeypatch.setitem(SITE_PARSERS, "no-urls-found-parser", not_found_parser)


def test_parse_ad_listing_page(parsers):
    assert parse_ad_listing_page("fake-parser", "<html>") == ["test-url1", "test-url2"]
    assert parse_ad_listing_page("no-urls-found-parser", "<html>") == []
    assert parse_ad_listing_page("no domain", "<html>") == []


def test_parse_sitemap(parsers, monkeypatch):
    mock_table = MagicMock()
    monkeypatch.setattr("__app__.sitemapparser.sitemapparser.TABLE", mock_table)
    # Happy path
    test_message = {
        "sitemapping-page": "<html>",
        "domain": "fake-parser",
        "metadata": {"meta": "data"},
    }
    parse_sitemap(test_message)
    mock_table.batch_merge_ad_listings.assert_called_with(
        ["test-url1", "test-url2"], "fake-parser", {"meta": "data"}
    )

    # No ads found
    mock_table.reset_mock()
    test_message = {
        "sitemapping-page": "<html>",
        "domain": "no-urls-found-parser",
        "metadata": {"meta": "data"},
    }
    mock_table.batch_merge_ad_listings.assert_not_called()
