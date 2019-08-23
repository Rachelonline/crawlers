import requests
import random
from time import sleep
from utils.headers import get_headers
import logging

MAX_RETRIES = 4

def no_retry_get(url, params=None):
    headers = get_headers()
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response

def get_url(url):
    """
    This is a pretty basic backoff with jitter. We can't use the backoff module
    because it's a sync function inside a co-routine.
    """
    attempts = 0
    while True:
        try:
            return no_retry_get(url)
        except requests.exceptions.RequestException as e:
            # jittered expo backoff
            sleeptime = random.uniform(0, 2**attempts)
            attempts += 1
            logging.info("attempt %s sleeping %s retrying %s", attempts, sleeptime, url)
            sleep(sleeptime)

            if attempts >= MAX_RETRIES:
                logging.info("giving up after attempt %s url %s", attempts, url)
                raise e
