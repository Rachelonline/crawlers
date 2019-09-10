import json
from typing import List
import logging
from azure.cosmosdb.table.tableservice import TableService, TableBatch
from utils.table.base_table import BaseAzureTable, encode_url, decode_url


MAX_BATCH_SIZE = 90


def chunk(l):
    # Break up the list into chunks
    for i in range(0, len(l), MAX_BATCH_SIZE):
        yield l[i : i + MAX_BATCH_SIZE]


class AdListingTable(BaseAzureTable):
    _table_name = "adlistings"

    def ad_listings(self) -> dict:
        for entity in self.table_service.query_entities(self._table_name):
            yield {
                "url": decode_url(entity.RowKey),
                "metadata": json.loads(entity.metadata),
            }

    def get_ad_listing_url(self, ad_listing_url: str, domain: str) -> dict:
        filter_str = f"PartitionKey eq '{encode_url(domain)}' and RowKey eq '{encode_url(ad_listing_url)}'"
        entities = self.table_service.query_entities(
            self._table_name, filter=filter_str, num_results=1
        )
        return [entity for entity in entities]

    def batch_merge_ad_listings(
        self, ad_listing_urls: List, domain: str, metadata: dict
    ) -> None:
        for ad_listing_url_chunk in chunk(ad_listing_urls):
            with self.table_service.batch(self._table_name) as batch:
                for ad_listing_url in ad_listing_url_chunk:
                    existing_ad_listing_url = self.get_ad_listing_url(ad_listing_url, domain)
                    if existing_ad_listing_url:
                        continue
                    logging.info("New ad listing url found for %s - %s", domain, ad_listing_url)
                    batch.insert_or_merge_entity(
                        {
                            "PartitionKey": encode_url(domain),
                            "RowKey": encode_url(ad_listing_url),
                            "metadata": json.dumps(metadata),
                        }
                    )
