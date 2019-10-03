import os
import sys
import logging
import json
from argparse import ArgumentParser, ArgumentTypeError
from azure.servicebus import ServiceBusClient, Message

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

CONNECTION = os.environ["SB_CONN_STR"]


def build_site_map_parse_msg(path, domain):
    with open(path) as html_f:
        url = html_f.read()
    return {"sitemapping-page": url, "domain": domain, "metadata": {"domain": domain, "manual-job": True}}


def main():
    parser = ArgumentParser(description="Manually load a site map parse job")
    parser.add_argument("domain", type=str, help="Domain to parse the site map.")
    parser.add_argument("path", type=str, help="Path (local) for file to parse")

    args = parser.parse_args()
    site_map_parse_job = build_site_map_parse_msg(args.path, args.domain)
    logging.info("Adding job to site map parse queue: %s", site_map_parse_job)
    client = ServiceBusClient.from_connection_string(CONNECTION)
    queue = client.get_queue("siteparse")
    queue.send(Message(json.dumps(site_map_parse_job)))


if __name__ == "__main__":
    main()
