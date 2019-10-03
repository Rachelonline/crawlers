import random
from copy import deepcopy

HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-us",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
]


def get_headers():
    headers = deepcopy(HEADERS)
    headers.update({"User-Agent": random.choice(USER_AGENTS)})
    return headers
