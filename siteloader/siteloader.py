from typing import List
import logging

SITES_TO_MAP = [
    ('cityxguide.com', {'domain': 'cityxguide.com'}),
    ('capleasures.com', {'domain': 'capleasures.com'}),
    ('backpage.ly', {'domain': 'backpage.ly'}),
    ('gfemonkey.com', {'domain': 'gfemonkey.com'}),
    ('eccie.net', {'domain': 'eecie.net'}),
]

def sitemapping_jobs() -> List[dict]:
    jobs = []
    for domain, metadata in SITES_TO_MAP:
        job = {
            'domain': domain,
            'metadata': metadata,
        }
        jobs.append(job)
        logging.info("queuing sitemapping for %s", domain)
    logging.info("queued total %s sitemapping jobs", len(jobs))
    return jobs

