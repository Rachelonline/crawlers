import json
import os
from base64 import b64encode

from azure.servicebus import ServiceBusClient
from azure.servicebus.common.errors import MessageAlreadySettled

CONNECTION = os.environ["SB_CONN_STR"]

def clear_queue(queue_name: str, domain: str, variant: str) -> None:
    print(f"BEGIN: Removing {variant} messages from {queue_name} for {domain}")
    client = ServiceBusClient.from_connection_string(CONNECTION)
    queue = client.get_queue(queue_name)
    total = 0

    receive = {"active": queue.get_receiver, "deadletter": queue.get_deadletter_receiver}
    with receive[variant](
        prefetch=200, mode=1, idle_timeout=5
        # mode=2 means it will delete on receive. We generally want that for perfomance
        # but if you want to look at the messages set mode=1 (Peek)
    ) as receiver:
        for msg in receiver:
            msg_data = json.loads(next(msg.body).decode("utf8"))
            if domain in msg_data["domain"]:
                try:
                    msg.complete()
                    print(msg_data)
                    total += 1
                except MessageAlreadySettled:
                    pass
    print(f"END: Removed {total} messages from {queue_name} for {domain}")
