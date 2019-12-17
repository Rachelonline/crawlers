"""
This is used to disable crawling on a domain.
"""

from argparse import ArgumentParser
from base64 import urlsafe_b64encode, urlsafe_b64decode
import json
import os
from azure.cosmosdb.table.tableservice import TableService
from azure.servicebus import ServiceBusClient
from azure.servicebus.common.errors import MessageAlreadySettled

CONNECTION = os.environ["SB_CONN_STR"]
TABLE_NAME = "adlistings"
QUEUE_NAME = "regioncrawl"

def encode_url(url: str) -> str:
    return urlsafe_b64encode(bytes(url, "utf-8")).decode("utf-8")


def decode_url(b64_string: str) -> str:
    return urlsafe_b64decode(b64_string).decode("utf-8")


def disable_ad_listing(domain_to_disable: str) -> None:
    table_service = TableService(
        account_name="picrawling", account_key=os.environ["TABLE_ACCESS_KEY"]
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

def clear_adlisting_crawl_queue(domain_to_disable: str) -> None:
    print(f"Removing ad listing crawls from the queue for {domain_to_disable}")
    client = ServiceBusClient.from_connection_string(CONNECTION)
    queue = client.get_queue(QUEUE_NAME)

    total = 0
    # mode=2 means it will delete on receive. We generally want that for perfomance
    # but if you want to look at the messages set mode=1 (Peek)
    with queue.get_receiver(
        prefetch=200, mode=1, idle_timeout=5
    ) as receiver:
        for msg in receiver:
            msg_data = json.loads(next(msg.body).decode("utf8"))
            if domain_to_disable in msg_data["domain"]:
                try:
                    msg.complete()
                    print(msg_data)
                    total += 1
                except MessageAlreadySettled:
                    pass
    print(f"Removed {total} ad listing crawls from the queue for {domain_to_disable}")


def main():
    parser = ArgumentParser(
        description="Temporary disable crawling on a domain"
    )
    parser.add_argument(
        "domain", type=str, help=f"domain to disable"
    )
    args = parser.parse_args()

    disable_ad_listing(args.domain)
    clear_adlisting_crawl_queue(args.domain)


if __name__ == "__main__":
    main()
