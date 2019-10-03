import logging
from __app__.utils.table.adlisting import AdListingTable


def ad_listing_loader():
    ad_listing_jobs = []
    table = AdListingTable()
    for ad_listing_job in table.ad_listings():
        logging.info("load job %s", ad_listing_job)
        ad_listing_jobs.append(ad_listing_job)
    return ad_listing_jobs


