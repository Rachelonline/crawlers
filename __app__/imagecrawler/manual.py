import os
import sys
import logging
import json
from argparse import ArgumentParser, ArgumentTypeError
from azure.servicebus import ServiceBusClient, Message

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

CONNECTION = os.environ["SB_CONN_STR"]


def build_ad_crawl_msg(url, domain):
    return {
        "ad-url": url,
        "domain": domain,
        "metadata": {"domain": domain, "manual-job": True},
    }


def main():
    parser = ArgumentParser(description="Manually crawl an ad page")
    parser.add_argument("domain", type=str, help="Domain to crawl the ad.")
    parser.add_argument("url", type=str, help="url for the ad to crawl")
    args = parser.parse_args()

    ad_listing_map_crawl_job = build_ad_crawl_msg(args.url, args.domain)

    logging.info("Adding job to ad crawl queue: %s", ad_listing_map_crawl_job)
    client = ServiceBusClient.from_connection_string(CONNECTION)
    queue = client.get_queue("pagecrawl")
    queue.send(Message(json.dumps(ad_listing_map_crawl_job)))


if __name__ == "__main__":
    main()
