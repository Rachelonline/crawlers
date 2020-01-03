"""
Reprocess location data. This is a one-off script to backfill all of our data with geocoding.

Uses multiprocessing for parallelism. Be sure to bump up the db throughput before running.

Unmaintained
"""
import os
from azure.cosmos.cosmos_client import CosmosClient
from __app__.utils.locations.geocode import get_location
from __app__.processor import geocode
import multiprocessing as mp


def ads(client):

    query = {
        "query": """
            SELECT VALUE
            c
            FROM c
            WHERE NOT IS_DEFINED(c.location) AND (c.domain ='megapersonals.eu' OR c.domain = 'vipgirlfriend.com' OR c.domain = 'escortdirectory.com')
        """
    }

    all_ads = client.QueryItems(
        "dbs/crawling/colls/ads", query, {"enableCrossPartitionQuery": True}
    )
    return all_ads


CLIENT = None


def init():
    global CLIENT
    CLIENT = CosmosClient(
        "https://crawling.documents.azure.com:443/",
        {"masterKey": os.environ["COSMOS_KEY"]},
    )


def update_location(ad):
    ad = geocode(ad)
    CLIENT.UpsertItem(
        f"dbs/crawling/colls/ads/", ad, options={"disableAutomaticIdGeneration": True}
    )


def main():
    client = CosmosClient(
        "https://crawling.documents.azure.com:443/",
        {"masterKey": os.environ["COSMOS_KEY"]},
    )
    with mp.Pool(initializer=init, processes=16) as pool:
        count = 0
        for _ in pool.imap(update_location, ads(client)):
            count += 1
            if count % 500 == 0:
                print(f"processing {count}")


if __name__ == "__main__":
    main()
