import json
from typing import List
from azure.cosmosdb.table.tableservice import TableService, TableBatch
from base64 import urlsafe_b64encode, urlsafe_b64decode

ACCOUNT_KEY = ""
ACCOUNT_NAME = "picrawling"


def encode_url(url: str) -> str:
    """ We encode urls because azure table RowKeys won't allow slashes (thus raw urls)"""
    return urlsafe_b64encode(bytes(url, "utf-8")).decode("utf-8")


def decode_url(b64_string: str) -> str:
    return urlsafe_b64decode(b64_string).decode("utf-8")


class BaseAzureTable:
    def __init__(self) -> None:
        self._table_service = None

    @property
    def table_service(self):
        if self._table_service is None:
            self._table_service = TableService(
                account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY
            )
        return self._table_service
