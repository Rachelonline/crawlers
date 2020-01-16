import pytest
from tests.fixtures.no_network import *
from __app__.utils.network.cookies import get_cookies


def test_get_cookies():
    assert get_cookies("https://megapersonals.eu") == {"confirmAge": "2"}
    assert get_cookies("https://google.com") is None
