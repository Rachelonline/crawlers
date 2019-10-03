import pytest
from tests.fixtures.no_network import *
from __app__.siteloader.siteloader import sitemapping_jobs


def test_sitemapping_jobs(monkeypatch):
    test_sites_to_map = [
        ("test", {"domain": "test"}),
        ("test2", {"domain": "test2"}),
        ("test3", {"domain": "test3"}),
    ]
    monkeypatch.setattr("__app__.siteloader.siteloader.SITES_TO_MAP", test_sites_to_map)

    expected = [
        {"domain": "test", "metadata": {"domain": "test"}},
        {"domain": "test2", "metadata": {"domain": "test2"}},
        {"domain": "test3", "metadata": {"domain": "test3"}},
    ]
    assert sitemapping_jobs() == expected
