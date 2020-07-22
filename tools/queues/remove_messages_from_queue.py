import json
import os
from argparse import ArgumentParser
from cleaner import clear_queue

def main():
    parser = ArgumentParser(
        description="Remove all active and deadletter messages from queues that require a connection to the domain"
    )
    parser.add_argument(
        "domain", type=str, help=f"domain to disable"
    )
    parser.add_argument(
        "queue", type=str, help=f"name of the queue"
    )
    parser.add_argument(
        "mode", type=str, help=f"active or deadletter"
    )
    args = parser.parse_args()

    clear_queue(args.queue, args.domain, args.mode)

if __name__ == "__main__":
    main()
