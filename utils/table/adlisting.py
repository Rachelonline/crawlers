import json
from typing import List
from azure.cosmosdb.table.tableservice import TableService, TableBatch
from base64 import urlsafe_b64encode, urlsafe_b64decode

ACCOUNT_KEY = ""
MAX_BATCH_SIZE = 90


def encode_url(url: str) -> str:
    """ We encode urls because azure table RowKeys won't allow slashes (thus raw urls)"""
    return urlsafe_b64encode(bytes(url, "utf-8")).decode("utf-8")


def decode_url(b64_string: str) -> str:
    return urlsafe_b64decode(b64_string).decode("utf-8")


class AdListingTable:
    _table_name = "adlistings"

    def __init__(self) -> None:
        self._table_service = None

    @property
    def table_service(self):
        if self._table_service is None:
            self._table_service = TableService(
                account_name="picrawling", account_key=ACCOUNT_KEY
            )
        return self._table_service

    def ad_listings(self) -> dict:
        for entity in self.table_service.query_entities(
            self._table_name, filter="enabled eq true"
        ):
            yield {
                "url": decode_url(entity.RowKey),
                "metadata": json.loads(entity.metadata),
            }

    def batch_merge_ad_listings(
        self, ad_listing_urls: List, domain: str, metadata: dict
    ) -> None:
        counter = 0  # Batch can only do 100 items at a time

        with self.table_service.batch(self._table_name) as batch:
            for ad_listing_url in ad_listing_urls:
                counter += 1
                batch.insert_or_merge_entity(
                    {
                        "PartitionKey": domain,
                        "RowKey": encode_url(ad_listing_url),
                        "metadata": json.dumps(metadata),
                    }
                )
                if counter >= MAX_BATCH_SIZE:
                    _ = self.table_service.commit_batch(
                        self._table_name, batch
                    )  # TODO: check for errors
                    counter = 0
