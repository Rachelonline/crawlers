import logging
from __app__.utils.table.adlisting import AdListingTable
from __app__.utils.metrics.metrics import get_client, enable_logging


def ad_listing_loader():
    azure_tc = get_client()
    enable_logging()
    ad_listing_jobs = []
    table = AdListingTable()
    for ad_listing_job in table.ad_listings():
        logging.info("load job %s", ad_listing_job)
        ad_listing_jobs.append(ad_listing_job)
        azure_tc.track_metric(
            "adlisting-load", 1, properties={"domain": ad_listing_job["domain"]}
        )
    azure_tc.flush()
    return ad_listing_jobs
