import logging
import json
import azure.functions as func

from __app__.sitemapparser.sitemapparser import parse_sitemap


def main(inmsg: func.ServiceBusMessage) -> None:
    message = json.loads(inmsg.get_body().decode("utf-8"))
    parse_sitemap(message)
