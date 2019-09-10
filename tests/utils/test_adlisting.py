import pytest
import json
from unittest.mock import MagicMock, call
from tests.fixtures.no_network import no_requests, no_azure_table_service

from utils.table.adlisting import AdListingTable


class Entity:
    def __init__(self, rowkey, metadata) -> None:
        self.RowKey = rowkey
        self.metadata = json.dumps(metadata)


@pytest.fixture
def mock_table_service(monkeypatch):
    mock_table_service = MagicMock()

    def mock_table(*args, **kwargs):
        return mock_table_service

    monkeypatch.setattr("utils.table.base_table.TableService", mock_table)
    return mock_table_service


def test_ad_listings(mock_table_service, monkeypatch):
    entites = [
        Entity("aHR0cDovL3d3dy5nb29nbGUuY29t", {"meta": "data1"}),
        Entity("aHR0cDovL3d3dy5nb29nbGUuY29t", {"meta": "data2"}),
        Entity("aHR0cDovL3d3dy5nb29nbGUuY29t", {"meta": "data3"}),
    ]
    mock_table_service.query_entities.return_value = entites
    expected = [
        {"url": "http://www.google.com", "metadata": {"meta": "data1"}},
        {"url": "http://www.google.com", "metadata": {"meta": "data2"}},
        {"url": "http://www.google.com", "metadata": {"meta": "data3"}},
    ]

    ad_listing_table = AdListingTable()
    actual = [x for x in ad_listing_table.ad_listings()]
    assert expected == actual

    # We also want to check the filter is correct
    mock_table_service.query_entities.assert_called_with(
        "adlistings", filter="enabled eq true"
    )


def test_batch_merge_ad_listings(mock_table_service, monkeypatch):
    urls = ["test1", "test2", "test3"]
    domain = "test-domain"
    metadata = {"meta": "data"}

    ad_listing_table = AdListingTable()
    ad_listing_table.batch_merge_ad_listings(urls, domain, metadata)

    # This bit of uglyness is because we are using batch as a context manager so we need to do the __enter__ etc.
    ad_listing_table.table_service.batch.return_value.__enter__.return_value.insert_or_merge_entity.assert_has_calls(
        [
            call(
                {
                    "PartitionKey": "test-domain",
                    "RowKey": "dGVzdDE=",
                    "metadata": '{"meta": "data"}',
                }
            ),
            call(
                {
                    "PartitionKey": "test-domain",
                    "RowKey": "dGVzdDI=",
                    "metadata": '{"meta": "data"}',
                }
            ),
            call(
                {
                    "PartitionKey": "test-domain",
                    "RowKey": "dGVzdDM=",
                    "metadata": '{"meta": "data"}',
                }
            ),
        ]
    )

    # Test max batch size
    monkeypatch.setattr("utils.table.adlisting.MAX_BATCH_SIZE", 1)
    ad_listing_table.table_service.reset_mock()
    ad_listing_table.batch_merge_ad_listings(urls, domain, metadata)

    # The max batch size is 1 so we should see 3 commit batches
    assert ad_listing_table.table_service.batch.call_count == 3
