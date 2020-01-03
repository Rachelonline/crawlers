import json
import azure.functions as func
from __app__.utils.metrics.metrics import get_client, enable_logging
from __app__.utils.queue.message import decode_message
from __app__.utils.locations.geocode import get_location


def geocode(message: dict) -> dict:
    ad_location = message["ad-data"].get("location")
    adlisting_location = message.get("ad-listing-data", {}).get("location")
    if adlisting_location:
        ad_location = f"{adlisting_location} {ad_location}"
    location = get_location(ad_location)
    message["location"] = location
    return message


def main(inmsg: func.ServiceBusMessage, doc: func.Out[func.Document]) -> None:
    azure_tc = get_client()
    enable_logging()

    message = decode_message(inmsg)
    message = geocode(message)

    doc.set(func.Document.from_json(json.dumps(message)))

    azure_tc.track_metric("ad-processed", 1, properties={"domain": message["domain"]})
    azure_tc.flush()
