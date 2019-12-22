import pytest
import json
from unittest.mock import MagicMock
from datetime import datetime
from tests.fixtures.no_network import *

from __app__.adcrawler.adcrawler import crawl_ad


@pytest.fixture(autouse=True)
def mock_uuid_storage_url(monkeypatch):
    monkeypatch.setattr("__app__.utils.storage.ads.uuid4", lambda: "uuid")


@pytest.fixture(autouse=True)
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def utcnow(cls):
            return datetime(2525, 1, 1)

    monkeypatch.setattr("__app__.adcrawler.adcrawler.datetime", mydatetime)


def test_crawl_ad(monkeypatch):
    mock_get_url = MagicMock()
    mock_get_url.return_value.text = "test_page"
    monkeypatch.setattr("__app__.adcrawler.adcrawler.get_url", mock_get_url)
    mock_table = MagicMock()
    monkeypatch.setattr("__app__.adcrawler.adcrawler.TABLE", mock_table)
    mock_table.is_crawled.return_value = False

    input_data = {
        "ad-url": "test_url",
        "domain": "test-domain",
        "metadata": {"domain": "test-domain", "other": "metadata"},
    }

    expected = {
        "ad-url": "test_url",
        "ad-page-blob": "https://blob.store/ads/uuid",
        "domain": "test-domain",
        "metadata": {
            "ad-crawled": "2525-01-01T00:00:00",
            "domain": "test-domain",
            "other": "metadata",
        },
    }

    assert crawl_ad(input_data) == expected
    mock_table.is_crawled.assert_called()
    mock_table.mark_crawled.assert_called_with(
        "test_url",
        "https://blob.store/ads/uuid",
        {
            "ad-crawled": "2525-01-01T00:00:00",
            "domain": "test-domain",
            "other": "metadata",
        },
    )


def test_dont_crawl(monkeypatch):
    mock_get_url = MagicMock()
    monkeypatch.setattr("__app__.adcrawler.adcrawler.get_url", mock_get_url)
    mock_table = MagicMock()
    monkeypatch.setattr("__app__.adcrawler.adcrawler.TABLE", mock_table)
    mock_table.is_crawled.return_value = True

    input_data = {
        "ad-url": "test_url",
        "domain": "test-domain",
        "metadata": {"domain": "test-domain", "other": "metadata"},
    }
    assert crawl_ad(input_data) is None
    mock_get_url.assert_not_called()
