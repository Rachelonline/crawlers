import json
from typing import List
from azure.common import AzureMissingResourceHttpError
from __app__.utils.table.base_table import BaseAzureTable, encode_url


class AdsTable(BaseAzureTable):
    _table_name = "ads"

    def is_crawled(self, url: str) -> bool:
        try:
            encoded = encode_url(url)
            _ = self.table_service.get_entity(self._table_name, encoded, encoded)
            return True
        except AzureMissingResourceHttpError:
            return False

    def mark_crawled(self, url: str, blob_uri: str, metadata: dict) -> None:
        self.table_service.insert_or_merge_entity(
            self._table_name,
            {
                "PartitionKey": encode_url(url),
                "RowKey": encode_url(url),
                "blob": blob_uri,
                "crawledon": metadata["ad-crawled"],
                "metadata": json.dumps(metadata),
            },
        )

    def mark_parsed(self, url: str, metadata: dict, image_urls: List[str]) -> None:
        entity = {
            "PartitionKey": encode_url(url),
            "RowKey": encode_url(url),
            "parsedon": metadata["ad-parsed"],
            "metadata": json.dumps(metadata),
        }
        if image_urls:
            entity.update({"imageurls": json.dumps(image_urls)})

        # Note: somewhat dangerous as it assumes that it's already in the table for being crawled
        #  which should always be true (famous last words)
        self.table_service.merge_entity(self._table_name, entity)
