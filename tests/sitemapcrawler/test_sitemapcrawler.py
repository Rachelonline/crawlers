import pytest
from unittest.mock import MagicMock
from tests.fixtures.no_network import *
from __app__.sitemapcrawler.sitemapcrawler import sitemap, SITE_MAP_CRAWLERS


def domain_mock(monkeypatch, domain: str) -> MagicMock:
    mock_mapper = MagicMock()
    mock_mapper.return_value.get_ad_listing_page.return_value = f"url-{domain}"
    mock_mapper.return_value.extra_metadata.return_value = {
        "site-map": "test-time-stamp"
    }
    monkeypatch.setitem(SITE_MAP_CRAWLERS, domain, mock_mapper)
    return mock_mapper


@pytest.fixture(autouse=True)
def mock_mappers(monkeypatch):
    domain_mock(monkeypatch, "cityxguide.com")


def test_sitemapping_jobs(mock_mappers):
    input_data = {"domain": "cityxguide.com", "metadata": {"domain": "cityxguide.com"}}
    expected = {
        "domain": "cityxguide.com",
        "sitemapping-page": "url-cityxguide.com",
        "metadata": {"domain": "cityxguide.com", "site-map": "test-time-stamp"},
    }

    assert sitemap(input_data) == expected

    input_data = {
        "domain": "no-parser-domain",
        "metadata": {"domain": "cityxguide.com"},
    }
    assert sitemap(input_data) is None
