import pytest
from tests.fixtures.no_network import *
from __app__.utils.network.headers import get_headers


@pytest.fixture(autouse=True)
def headers_fixtures(monkeypatch):
    headers = {"headers": "to use"}
    monkeypatch.setattr("__app__.utils.network.headers.HEADERS", headers)
    user_agents = ["useragent"]
    monkeypatch.setattr("__app__.utils.network.headers.USER_AGENTS", user_agents)


def test_get_headers(headers_fixtures):
    expected = {"headers": "to use", "User-Agent": "useragent"}
    assert get_headers() == expected
