import pytest
from tests.fixtures.no_network import *

from __app__.adlistingloader.adlistingloader import ad_listing_loader


def test_ad_listing_loader(monkeypatch):
    mock_ad_listing = [
        {"url": "test", "domain": "test-domain", "metadata": {"meta": "data"}},
        {"url": "test2", "domain": "test-domain", "metadata": {"meta": "data"}},
        {"url": "test3", "domain": "test-domain", "metadata": {"meta": "data"}},
    ]
    monkeypatch.setattr(
        "__app__.adlistingloader.adlistingloader.AdListingTable.ad_listings",
        lambda _: mock_ad_listing,
    )

    expected = [
        {"url": "test", "domain": "test-domain", "metadata": {"meta": "data"}},
        {"url": "test2", "domain": "test-domain", "metadata": {"meta": "data"}},
        {"url": "test3", "domain": "test-domain", "metadata": {"meta": "data"}},
    ]
    assert ad_listing_loader() == expected
