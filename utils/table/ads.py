import json
from typing import List
from azure.cosmosdb.table.tableservice import TableService, TableBatch
from azure.common import AzureMissingResourceHttpError
from base64 import urlsafe_b64encode, urlsafe_b64decode

ACCOUNT_KEY = ""
MAX_BATCH_SIZE = 90


def encode_url(url: str) -> str:
    """ We encode urls because azure table RowKeys won't allow slashes (thus raw urls)"""
    return urlsafe_b64encode(bytes(url, "utf-8")).decode("utf-8")


def decode_url(b64_string: str) -> str:
    return urlsafe_b64decode(b64_string).decode("utf-8")


class AdsTable:
    _table_name = "ads"

    def __init__(self) -> None:
        self._table_service = None

    @property
    def table_service(self):
        if self._table_service is None:
            self._table_service = TableService(
                account_name="picrawling", account_key=ACCOUNT_KEY
            )
        return self._table_service

    def is_crawled(self, url: str) -> bool:
        try:
            encoded = encode_url(url)
            _ = self.table_service.get_entity(self._table_name, encoded, encoded)
            return True
        except AzureMissingResourceHttpError:
            return False

