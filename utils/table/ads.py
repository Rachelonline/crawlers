import json
from azure.common import AzureMissingResourceHttpError
from utils.table.base_table import BaseAzureTable, encode_url


class AdsTable(BaseAzureTable):
    _table_name = "ads"

    def is_crawled(self, url: str) -> bool:
        try:
            encoded = encode_url(url)
            _ = self.table_service.get_entity(self._table_name, encoded, encoded)
            return True
        except AzureMissingResourceHttpError:
            return False
