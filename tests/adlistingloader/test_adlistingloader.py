import pytest
from tests.fixtures.no_network import no_requests

from adlistingloader.adlistingloader import ad_listing_loader


def test_ad_listing_loader(monkeypatch):
    mock_ad_listing = [{"domain": "test"}, {"domain": "test2"}, {"domain": "test3"}]
    monkeypatch.setattr(
        "adlistingloader.adlistingloader.AdListingTable.ad_listings",
        lambda _: mock_ad_listing,
    )

    expected = [{"domain": "test"}, {"domain": "test2"}, {"domain": "test3"}]
    assert ad_listing_loader() == expected
