import os
import json
from azure.cosmosdb.table.tableservice import TableService
from base64 import urlsafe_b64encode, urlsafe_b64decode

DOMAIN = "capleasures.com"
TO_DISABLE = [
    "https://capleasures.com/c/alberta",
    "https://capleasures.com/c/britishcolumbia",
    "https://capleasures.com/c/manitoba",
    "https://capleasures.com/c/newbrunswick",
    "https://capleasures.com/c/stjohns",
    "https://capleasures.com/c/yellowknife",
    "https://capleasures.com/c/halifax",
    "https://capleasures.com/c/ontario",
    "https://capleasures.com/c/quebec",
    "https://capleasures.com/c/saskatchewan",
    "https://capleasures.com/c/yukon",
]


def encode_url(url: str) -> str:
    return urlsafe_b64encode(bytes(url, "utf-8")).decode("utf-8")


def decode_url(b64_string: str) -> str:
    return urlsafe_b64decode(b64_string).decode("utf-8")


def main():
    domain = "capleasures.com"
    table_service = TableService(
        account_name="picrawling", account_key=os.environ["TABLE_ACCESS_KEY"]
    )

    for disable_url in TO_DISABLE:
        table_service.merge_entity(
            "adlistings",
            {
                "PartitionKey": encode_url(domain),
                "RowKey": encode_url(disable_url),
                "enabled": False,
            },
        )


if __name__ == "__main__":
    main()
