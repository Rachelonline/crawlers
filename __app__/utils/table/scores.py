import json
from datetime import datetime
from typing import List
from __app__.utils.table.base_table import BaseAzureTable, encode_url


class ScoresTable(BaseAzureTable):
    _table_name = "scores"


    def save_score(self, phone_number: str, metadata: dict) -> None:
        """
        Save the scores for a particular phone number. uses the 
        current Y-M-D as the partition_key so that we can have
        daily records for each number if they are visited multiple times
        """
        self.table_service.insert_or_merge_entity(
            self._table_name,
            {
                "PartitionKey": encode_url(datetime.now().strftime("%Y-%m-%d")),
                "RowKey": encode_url(phone_number),
                "scoredon": metadata["ad-scored"],
                "metadata": json.dumps(metadata),
            }
        )