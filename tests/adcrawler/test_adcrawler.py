import pytest
from unittest.mock import MagicMock
from datetime import datetime
from tests.fixtures.no_network import no_requests

from adcrawler.adcrawler import crawl_ad


@pytest.fixture(autouse=True)
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return datetime(2525, 1, 1)

    monkeypatch.setattr("adcrawler.adcrawler.datetime", mydatetime)


def test_crawl_ad_(monkeypatch):
    mock_get_url = MagicMock()
    mock_get_url.return_value.text = "test_page"

    monkeypatch.setattr("adcrawler.adcrawler.get_url", mock_get_url)

    input_data = {
        "ad-url": "test_url",
        "metadata": {"domain": "test-domain", "other": "metadata"},
    }

    expected = {
        "ad-page": "test_page",
        "metadata": {
            "ad-crawled": "2525-01-01T00:00:00",
            "domain": "test-domain",
            "other": "metadata",
        },
    }

    assert crawl_ad(input_data) == expected
