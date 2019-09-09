import pytest
from tests.fixtures.no_network import no_requests, no_azure_table_service

from adlistingloader.adlistingloader import ad_listing_loader


def test_ad_listing_loader(monkeypatch):
    mock_ad_listing = [
        {"url": "test", "metadata": {"meta": "data"}},
        {"url": "test2", "metadata": {"meta": "data"}},
        {"url": "test3", "metadata": {"meta": "data"}},
    ]
    monkeypatch.setattr(
        "adlistingloader.adlistingloader.AdListingTable.ad_listings",
        lambda _: mock_ad_listing,
    )

    expected = [
        {"url": "test", "metadata": {"meta": "data"}},
        {"url": "test2", "metadata": {"meta": "data"}},
        {"url": "test3", "metadata": {"meta": "data"}},
    ]
    assert ad_listing_loader() == expected
