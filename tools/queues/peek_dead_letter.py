import json
import os
import logging
from base64 import b64encode

from argparse import ArgumentParser, ArgumentTypeError

from azure.servicebus import ServiceBusClient, Message
import azure.functions as func
from azure.storage.blob import BlobClient


CONNECTION = os.environ["SB_CONN_STR"]
QUEUE_NAMES = [
    "imagecrawl",
    "pagecrawl",
    "pageparse",
    "process",
    "regioncrawl",
    "regionparse",
    "sitecrawl",
    "siteparse",
]


def valid_queue_name(queue: str) -> str:
    if queue not in QUEUE_NAMES:
        raise ArgumentTypeError("Not a valid queue name. check --help")
    return queue


def reprocess_messages(queuename: str) -> None:
    logging.warning("Reprocessing dead letter on: %s", queuename)
    client = ServiceBusClient.from_connection_string(CONNECTION)
    queue = client.get_queue(queuename)

    total = 0
    # Get the dead letter messages
    dead_letter_msgs = []
    # mode=2 means it will delete on receive. We generally want that for perfomance
    # but if you want to look at the messages set mode=1 (Peek)
    with queue.get_deadletter_receiver(
        prefetch=200, mode=1, idle_timeout=5
    ) as receiver:
        for msg in receiver:
            print(next(msg.body))
            break


def main():
    parser = ArgumentParser(
        description="Move all dead letter messages back on the main queue, requires SB_CONN_STR to be set"
    )
    parser.add_argument(
        "queue", type=valid_queue_name, help=f"Must be one of {', '.join(QUEUE_NAMES)}"
    )
    args = parser.parse_args()
    reprocess_messages(args.queue)


if __name__ == "__main__":
    main()
