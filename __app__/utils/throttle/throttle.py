import os
from urllib.parse import urlparse
import redis

REDIS_HOST = "picrawling.redis.cache.windows.net"
REQUESTS_PER_BUCKET = 5
BUCKET_LENGTH = 4  # seconds


class Throttled(Exception):
    def __init__(self, delay, domain):
        self.delay = delay
        self.domain = domain

    def __str__(self):
        return f"{self.delay}: {self.domain}"


def get_connection():
    return redis.Redis(
        host=REDIS_HOST, port=6380, db=0, password=os.environ["REDIS_KEY"], ssl=True
    )


def check_throttle(url, azure_tc=None):
    """
    A very basic rate limiter which will rate limit per domain.
      throws a Throttled when over. Throttled.delay is a *rough* estimate of when the rate
      rate limit is ready to be used again.
    """
    conn = get_connection()
    domain = "{uri.netloc}".format(uri=urlparse(url))

    current = conn.llen(domain)
    if current > REQUESTS_PER_BUCKET:
        total = conn.rpushx(f"{domain}-max", domain)
        estimated_delay = (total // REQUESTS_PER_BUCKET) * BUCKET_LENGTH
        if azure_tc:
            azure_tc.track_metric("throttled", 1, properties={"domain": domain})
        raise Throttled(estimated_delay, domain)

    if not conn.exists(domain):
        pipe = conn.pipeline()
        pipe.rpush(domain, domain)
        pipe.expire(domain, BUCKET_LENGTH)
        pipe.rpush(f"{domain}-max", domain)
        pipe.expire(f"{domain}-max", BUCKET_LENGTH)
        pipe.execute()
    else:
        pipe = conn.pipeline()
        pipe.rpushx(domain, domain)
        pipe.rpushx(f"{domain}-max", domain)
        pipe.execute()
