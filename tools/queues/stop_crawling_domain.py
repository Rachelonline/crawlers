"""
This is used to disable crawling on a domain.
"""

from argparse import ArgumentParser
from base64 import urlsafe_b64encode, urlsafe_b64decode
import json
import os
from azure.cosmosdb.table.tableservice import TableService
from cleaner import clear_queue

TABLE_NAME = "adlistings"

def encode_url(url: str) -> str:
    return urlsafe_b64encode(bytes(url, "utf-8")).decode("utf-8")


def decode_url(b64_string: str) -> str:
    return urlsafe_b64decode(b64_string).decode("utf-8")


def disable_ad_listing(domain_to_disable: str) -> None:
    table_service = TableService(
        account_name="picrawling", account_key=os.environ["TABLE_SERVICE_KEY"]
    )
    print(f"disabling ad listing crawling on {domain_to_disable}")
    count = 0
    for entity in table_service.query_entities(TABLE_NAME):
        url = decode_url(entity.RowKey)
        if domain_to_disable in url:
            table_service.merge_entity(
                TABLE_NAME,
                {
                    "PartitionKey": entity.PartitionKey,
                    "RowKey": entity.RowKey,
                    "enabled": False,
                },
            )
            count += 1
    print(f"disabled {count} ad listings on {domain_to_disable}")


def main():
    parser = ArgumentParser(
        description="Temporary disable crawling on a domain"
    )
    parser.add_argument(
        "domain", type=str, help=f"domain to disable"
    )
    args = parser.parse_args()

    disable_ad_listing(args.domain)
    clear_queue("regioncrawl", args.domain, "active")


if __name__ == "__main__":
    main()
