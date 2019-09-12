import pytest
import json
from unittest.mock import MagicMock, call
from tests.fixtures.no_network import no_requests, no_azure_table_service

from azure.common import AzureMissingResourceHttpError
from utils.table.ads import AdsTable


@pytest.fixture
def mock_table_service(monkeypatch):
    mock_table_service = MagicMock()

    def mock_table(*args, **kwargs):
        return mock_table_service

    monkeypatch.setattr("utils.table.base_table.TableService", mock_table)
    return mock_table_service


def test_is_crawled(mock_table_service):
    mock_table_service.get_entity.return_value = "yes"
    ads_table = AdsTable()
    assert ads_table.is_crawled("test-url") == True

    mock_table_service.get_entity.side_effect = AzureMissingResourceHttpError(
        "test", 404
    )
    ads_table = AdsTable()
    assert ads_table.is_crawled("test-url") == False


def test_mark_crawled(mock_table_service):
    ads_table = AdsTable()
    ads_table.mark_crawled("test-url", "blob-uri", {"meta": "data"})
    mock_table_service.insert_or_merge_entity.assert_called_with(
        "ads",
        {
            "PartitionKey": "dGVzdC11cmw=",
            "RowKey": "dGVzdC11cmw=",
            "blob": "blob-uri",
            "metadata": '{"meta": "data"}',
        },
    )


def test_mark_parsed(mock_table_service):
    ads_table = AdsTable()
    ads_table.mark_parsed("test-url", "parsed-on", [])
    mock_table_service.merge_entity.assert_called_with(
        "ads",
        {
            "PartitionKey": "dGVzdC11cmw=",
            "RowKey": "dGVzdC11cmw=",
            "parsed-on": "parsed-on",
        },
    )

    ads_table.mark_parsed("test-url", "parsed-on", ["test-img", "test-img2"])
    mock_table_service.merge_entity.assert_called_with(
        "ads",
        {
            "PartitionKey": "dGVzdC11cmw=",
            "RowKey": "dGVzdC11cmw=",
            "parsed-on": "parsed-on",
            "image-urls": ["test-img", "test-img2"],
        },
    )
