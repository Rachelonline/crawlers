import azure.functions as func
from __app__.utils.metrics.metrics import get_client, enable_logging
from __app__.utils.queue.message import decode_message


def main(inmsg: func.ServiceBusMessage, doc: func.Out[func.Document]) -> None:
    azure_tc = get_client()
    enable_logging()

    message = decode_message(inmsg)
    doc.set(func.Document.from_json(inmsg.get_body()))

    azure_tc.track_metric("ad-processed", 1, properties={"domain": message["domain"]})
    azure_tc.flush()
