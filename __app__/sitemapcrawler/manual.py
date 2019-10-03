import os
import sys
import logging
import json
from argparse import ArgumentParser, ArgumentTypeError
from azure.servicebus import ServiceBusClient, Message

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

CONNECTION = os.environ["SB_CONN_STR"]


def build_site_map_crawl_msg(domain):
    return {"domain": domain, "metadata": {"domain": domain, "manual-job": True}}


def main():
    parser = ArgumentParser(description="Manually site map crawl")
    parser.add_argument("--domain", type=str, help="Domain to crawl the site map.")

    args = parser.parse_args()
    site_map_crawl_job = build_site_map_crawl_msg(args.domain)
    logging.info("Adding job to site map crawl queue: %s", site_map_crawl_job)
    client = ServiceBusClient.from_connection_string(CONNECTION)
    queue = client.get_queue("sitecrawl")
    queue.send(Message(json.dumps(site_map_crawl_job)))


if __name__ == "__main__":
    main()
