import pytest
from unittest.mock import MagicMock
from tests.fixtures.no_network import *
from __app__.sitemapcrawler.sitemapcrawler import sitemap, SITEMAP_URL


@pytest.fixture(autouse=True)
def crawl_mocks(monkeypatch):
    mock_get_url = MagicMock()
    monkeypatch.setattr("__app__.sitemapcrawler.sitemapcrawler.get_url", mock_get_url)
    mock_get_url.return_value = "test-page"

    mock_datetime = MagicMock()
    monkeypatch.setattr("__app__.sitemapcrawler.sitemapcrawler.datetime", mock_datetime)
    mock_datetime.utcnow.return_value.replace.return_value.isoformat.return_value = (
        "test-time-stamp"
    )

    monkeypatch.setitem(SITEMAP_URL, "test-domain", "test-url")


def test_sitemapping_jobs(crawl_mocks):

    input_data = {"domain": "test-domain", "metadata": {"domain": "test-domain"}}
    expected = {
        "domain": "test-domain",
        "sitemapping-page": "test-page",
        "metadata": {"domain": "test-domain", "site-map": "test-time-stamp"},
    }

    assert sitemap(input_data) == expected

    input_data = {
        "domain": "no-parser-domain",
        "metadata": {"domain": "test-domain"},
    }
    assert sitemap(input_data) is None
