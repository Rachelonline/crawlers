from typing import List
import logging
from __app__.utils.metrics.metrics import get_client, enable_logging


SITES_TO_MAP = [
    ("cityxguide.com", {"domain": "cityxguide.com"}),
    ("capleasures.com", {"domain": "capleasures.com"}),
    ("backpage.ly", {"domain": "backpage.ly"}),
    ("gfemonkey.com", {"domain": "gfemonkey.com"}),
    ("eccie.net", {"domain": "eecie.net"}),
]


def sitemapping_jobs() -> List[dict]:
    azure_tc = get_client()
    enable_logging()

    jobs = []
    for domain, metadata in SITES_TO_MAP:
        job = {"domain": domain, "metadata": metadata}
        jobs.append(job)
        azure_tc.track_metric("sitemap-load", 1, properties={"domain": domain})
        logging.info("queuing sitemapping for %s", domain)
    logging.info("queued total %s sitemapping jobs", len(jobs))
    azure_tc.flush()
    return jobs
