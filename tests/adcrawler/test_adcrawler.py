import pytest
import json
from unittest.mock import MagicMock
from datetime import datetime
from tests.fixtures.no_network import *

from adcrawler.adcrawler import crawl_ad


@pytest.fixture(autouse=True)
def mock_uuid_storage_url(monkeypatch):
    monkeypatch.setattr("utils.ads.adstore.uuid4", lambda: "uuid")
    monkeypatch.setattr("utils.ads.adstore.STORAGE_URL", "blob.storage")


@pytest.fixture(autouse=True)
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return datetime(2525, 1, 1)

    monkeypatch.setattr("adcrawler.adcrawler.datetime", mydatetime)


def test_crawl_ad(monkeypatch):
    mock_get_url = MagicMock()
    mock_get_url.return_value.text = "test_page"
    monkeypatch.setattr("adcrawler.adcrawler.get_url", mock_get_url)
    mock_table = MagicMock()
    monkeypatch.setattr("adcrawler.adcrawler.TABLE", mock_table)
    mock_table.is_crawled.return_value = False

    input_data = {
        "ad-url": "test_url",
        "domain": "test-domain",
        "metadata": {"domain": "test-domain", "other": "metadata"},
    }

    expected = {
        "ad-url": "test_url",
        "ad-page-blob": "blob.storage/2525/01/01/test-domain/uuid",
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
        "blob.storage/2525/01/01/test-domain/uuid",
        {
            "ad-crawled": "2525-01-01T00:00:00",
            "domain": "test-domain",
            "other": "metadata",
        },
    )


def test_dont_crawl(monkeypatch):
    mock_get_url = MagicMock()
    monkeypatch.setattr("adcrawler.adcrawler.get_url", mock_get_url)
    mock_table = MagicMock()
    monkeypatch.setattr("adcrawler.adcrawler.TABLE", mock_table)
    mock_table.is_crawled.return_value = True

    input_data = {
        "ad-url": "test_url",
        "domain": "test-domain",
        "metadata": {"domain": "test-domain", "other": "metadata"},
    }
    assert crawl_ad(input_data) is None
    mock_get_url.assert_not_called()
