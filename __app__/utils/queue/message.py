import json
from typing import Union, List
import os
from sys import getsizeof
from uuid import uuid4
import azure.functions as func
from __app__.utils.storage.blob_store import save_blob, get_blob


MAX_MESSAGE_BYTES = 256_000 * 0.85  # 256kb azure max msg size with a 15% margin.


def get_blob_msg(message: dict) -> dict:
    return json.loads(get_blob(message["blob-message"]))


def put_blob_msg(message: dict) -> dict:
    blob_uri = save_blob(f"oversized-msgs/{str(uuid4())}", json.dumps(message))
    message = {"blob-message": blob_uri}
    return message


def decode_message(raw_message: func.ServiceBusMessage) -> dict:
    """
    Decodes the incoming message.
    """
    message = json.loads(raw_message.get_body().decode("utf-8"))
    if "blob-message" in message:
        message = get_blob_msg(message)
    return message


def _encode_single_msg(message: dict) -> str:
    # NOTE: This json dumping is a hack to see the size of the dict including all values
    #  There's prob a better way
    if getsizeof(json.dumps(message)) > MAX_MESSAGE_BYTES:
        message = put_blob_msg(message)

    return message


def encode_message(message: Union[dict, List[dict]]) -> str:
    """
    Encodes the message/messages so we can send it on to the next queue.

    If any message is above the azure service bus limit it is written
    to blob store and a pointer message is provided.

    This accepts list of messages, because the func.Out does as well
    """
    if isinstance(message, list):
        return json.dumps([_encode_single_msg(msg) for msg in message])

    return json.dumps(_encode_single_msg(message))
