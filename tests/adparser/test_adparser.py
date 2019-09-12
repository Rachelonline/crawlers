from datetime import datetime
import pytest
from unittest.mock import MagicMock
from tests.fixtures.no_network import *
from adparser.adparser import (
    AD_PARSERS,
    parse_ads,
    build_image_url_msgs,
    build_ad_process_msg,
    parse_ad,
)


@pytest.fixture(autouse=True)
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return datetime(2525, 1, 1)

    monkeypatch.setattr("adparser.adparser.datetime", mydatetime)


def fake_parser(page):
    return {"ad": "data"}, ["img-url"]


def not_found_parser(page):
    return {}, []


@pytest.fixture
def parsers(monkeypatch):
    monkeypatch.setitem(AD_PARSERS, "fake-parser", fake_parser)
    monkeypatch.setitem(AD_PARSERS, "no-ad-data-found-parser", not_found_parser)


def test_parse_ads(parsers):
    assert parse_ads("fake-parser", "<html>") == ({"ad": "data"}, ["img-url"])
    assert parse_ads("no-ad-data-found-parser", "<html>") == ({}, [])
    assert parse_ads("no domain", "<html>") == ({}, [])


def test_build_ad_process_msgs():
    test_msg = {
        "ad-url": "ad-url1",
        "ad-page-blob": "test-blob",
        "domain": "test",
        "metadata": {"meta": "data"},
    }
    ad_data = {"ad": "data"}

    expected = {
        "ad-url": "ad-url1",
        "ad-page-blob": "test-blob",
        "domain": "test",
        "ad-data": {"ad": "data"},
        "metadata": {"meta": "data"},
    }

    assert build_ad_process_msg(test_msg, ad_data) == expected


def test_build_image_url_msgs():
    test_msg = {
        "ad-url": "ad-url1",
        "ad-page-blob": "test-blob",
        "domain": "test",
        "metadata": {"meta": "data"},
    }
    urls = ["img-url1", "img-url3"]

    expected = [
        {
            "image-url": "img-url1",
            "domain": "test",
            "metadata": {"meta": "data"},
        },
        {
            "image-url": "img-url3",
            "domain": "test",
            "metadata": {"meta": "data"},
        },
    ]
    assert build_image_url_msgs(test_msg, urls) == expected


def test_parse_ad(monkeypatch):
    test_msg = {
        "ad-url": "ad-url1",
        "ad-page-blob": "test-blob",
        "domain": "test",
        "metadata": {"meta": "data"},
    }
    mock_parse = MagicMock()
    mock_parse.return_value = {"ad": "data"}, ["img-url"]
    monkeypatch.setattr("adparser.adparser.parse_ads", mock_parse)
    expected_ad_processer_msg = {
        "ad-url": "ad-url1",
        "ad-page-blob": "test-blob",
        "domain": "test",
        "metadata": {"meta": "data", "ad-parsed": "2525-01-01T00:00:00"},
        "ad-data": {"ad": "data"},
    }
    expected_img_url_msgs = [{
        "image-url": "img-url",
        "domain": "test",
        "metadata": {"meta": "data", "ad-parsed": "2525-01-01T00:00:00"},
    }]

    assert parse_ad(test_msg) == (expected_ad_processer_msg, expected_img_url_msgs)
