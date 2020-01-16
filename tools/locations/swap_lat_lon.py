"""
A one off script to fix my duckup where latitude and longitude were reversed.

Uses multiprocessing for parallelism. Be sure to bump up the db throughput before running.

Unmaintained.
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
            WHERE IS_DEFINED(c.location)
            AND NOT ST_ISVALID(c['location'])
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


def reverse_lat_lon(ad):
    if ad['location']:
        ad['location']['coordinates'] = ad['location']['coordinates'][::-1]
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
        for _ in pool.imap(reverse_lat_lon, ads(client)):
            count += 1
            if count % 500 == 0:
                print(f"processing {count}")


if __name__ == "__main__":
    main()
