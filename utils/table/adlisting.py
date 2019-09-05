import json
from azure.cosmosdb.table.tableservice import TableService
from base64 import urlsafe_b64encode, urlsafe_b64decode


def encode_url(url: str) -> str:
    """ We encode urls because azure table RowKeys won't allow slashes (thus raw urls)"""
    return urlsafe_b64encode(bytes(url, "utf-8")).decode("utf-8")


def decode_url(b64_string: str) -> str:
    return urlsafe_b64decode(b64_string).decode("utf-8")




class AdListingTable:
    _table_name = "adlistings"
    def __init__(self):
        self.table_service = TableService(
            account_name="picrawling",
            account_key="",
        )


    def ad_listings(self):
        for entity in self.table_service.query_entities(self._table_name, filter="enabled eq true"):
            yield {
                'url': decode_url(entity.RowKey),
                'metadata': json.loads(entity.metadata)
            }

