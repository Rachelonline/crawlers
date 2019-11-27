import os
import sys
import logging
import json
from argparse import ArgumentParser, ArgumentTypeError
from azure.servicebus import ServiceBusClient, Message

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

CONNECTION = os.environ["SB_CONN_STR"]


def main():
    parser = ArgumentParser(description="Manually load a job on the test-in-queue")
    parser.add_argument(
        "path", type=str, help="Path (local) json message to load on queue"
    )

    args = parser.parse_args()

    with open(args.path) as msg_f:
        message = json.load(msg_f)

    client = ServiceBusClient.from_connection_string(CONNECTION)
    queue = client.get_queue("test-in-queue")
    queue.send(Message(json.dumps(message)))


if __name__ == "__main__":
    main()
