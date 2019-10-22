import json
from typing import List
from azure.common import AzureMissingResourceHttpError
from __app__.utils.table.base_table import BaseAzureTable, encode_url


class ImagesTable(BaseAzureTable):
    _table_name = "images"

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

