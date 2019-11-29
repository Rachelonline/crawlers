import json
import os
import random
import logging
from azure.servicebus import ServiceBusClient, Message
from datetime import datetime, timedelta
from __app__.utils.network.network import CrawlError, NotFound
from __app__.utils.throttle.throttle import Throttled
from __app__.utils.queue.message import decode_message, encode_message


MAX_CRAWL_RETRIES = 5


def throttle(message, queue_name, delay=0):
    requeue_job(message, queue_name, delay=delay)


def error_retry(message, queue_name):
    retry_count = message.get("crawl_retries", 0)
    retry_count += 1

    # jittered expo backoff
    delay = random.uniform(0, 2 ** retry_count)

    message["crawl_retries"] = retry_count
    is_final = retry_count > MAX_CRAWL_RETRIES
    requeue_job(message, queue_name, delay=delay, final=is_final)


def not_found(message, queue_name):
    requeue_job(message, queue_name, final=True)


def requeue_job(message, queue_name, delay=0, final=False):
    client = ServiceBusClient.from_connection_string(os.environ["SB_CONN_STR"])
    if final:
        queue_name = f"{queue_name}-failed"
    queue = client.get_queue(queue_name)

    raw_message = Message(encode_message(message))
    with queue.get_sender() as sender:
        sender.schedule(datetime.utcnow() + timedelta(seconds=delay), raw_message)
        sender.send_pending_messages()


def crawl_job(raw_message, queue_name, crawl_f):
    """ Wraps a crawl job to manage retries and throttles """
    message = decode_message(raw_message)
    try:
        return crawl_f(message)
    except Throttled as err:
        throttle(message, queue_name, delay=err.delay)
    except CrawlError as err:
        error_retry(message, queue_name)
    except NotFound as err:
        not_found(message, queue_name)
    return
