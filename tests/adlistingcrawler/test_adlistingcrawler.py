import pytest
from unittest.mock import MagicMock
from datetime import datetime
from tests.fixtures.no_network import no_requests

from adlistingcrawler.adlistingcrawler import crawl_ad_listing


@pytest.fixture(autouse=True)
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return datetime(2525, 1, 1)

    monkeypatch.setattr("adlistingcrawler.adlistingcrawler.datetime", mydatetime)


def test_crawl_ad_listing(monkeypatch):
    mock_get_url = MagicMock()
    mock_get_url.return_value.text = "test_page"

    monkeypatch.setattr("adlistingcrawler.adlistingcrawler.get_url", mock_get_url)

    input_data = {
        "ad-listing-url": "test_url",
        "metadata": {"domain": "test-domain", "other": "metadata"},
    }

    expected = {
        "ad-listing-page": "test_page",
        "metadata": {
            "ad-listing-crawled": "2525-01-01T00:00:00",
            "domain": "test-domain",
            "other": "metadata",
        },
    }

    assert crawl_ad_listing(input_data) == expected
