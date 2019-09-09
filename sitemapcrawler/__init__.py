import logging
import json
import azure.functions as func

from sitemapper.sitemapper import sitemap


def main(inmsg: func.ServiceBusMessage, outmsg: func.Out[str]) -> None:
    message = json.loads(inmsg.get_body().decode("utf-8"))
    sitemap_parse_message = sitemap(message)
    outmsg.set(json.dumps(sitemap_parse_message))
