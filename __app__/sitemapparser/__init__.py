import azure.functions as func
from __app__.sitemapparser.sitemapparser import parse_sitemap
from __app__.utils.queue.message import decode_message


def main(inmsg: func.ServiceBusMessage) -> None:
    message = decode_message(inmsg)
    parse_sitemap(message)
