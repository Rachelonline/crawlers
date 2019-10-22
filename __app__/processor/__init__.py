import logging
import json
import azure.functions as func

def main(inmsg: func.ServiceBusMessage, doc: func.Out[func.Document]) -> None:
    #message = json.loads(inmsg.get_body().decode("utf-8"))
    doc.set(func.Document.from_json(inmsg.get_body()))
