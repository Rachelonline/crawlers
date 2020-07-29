import json
import os
import logging
from base64 import b64encode

from argparse import ArgumentParser, ArgumentTypeError
from azure.servicebus import ServiceBusClient, Message


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
        prefetch=200, mode=2, idle_timeout=5
    ) as receiver:
        for msg in receiver:
            msg_body = next(msg.body)
            if len(msg_body) < 5:
                continue
            dead_letter_msgs.append(Message(next(msg.body)))

            # Send if we have enough messages
            if len(dead_letter_msgs) >= 500:
                queue.send(dead_letter_msgs)
                logging.warning(
                    "%s messages moved back to queue", len(dead_letter_msgs)
                )
                total += len(dead_letter_msgs)
                dead_letter_msgs = []

    queue.send(dead_letter_msgs)
    total += len(dead_letter_msgs)
    logging.warning("\n----\nCompleted:\n%s messages moved back to queue", total)


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
