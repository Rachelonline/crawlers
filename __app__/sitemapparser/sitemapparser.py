import logging
from __app__.utils.table.adlisting import AdListingTable
from __app__.sitemapparser.sites.cityxguide_com import cityxguide_com
from __app__.utils.metrics.metrics import get_client, enable_logging


SITE_PARSERS = {"cityxguide.com": cityxguide_com}

TABLE = AdListingTable()


def parse_ad_listing_page(domain, page):
    parser = SITE_PARSERS.get(domain)
    if parser is None:
        logging.error("No site map parser for %s", domain)
        return []
    return parser(page)


def parse_sitemap(message):
    azure_tc = get_client()
    enable_logging()

    page = message["sitemapping-page"]
    domain = message["domain"]
    ad_listing_urls = parse_ad_listing_page(domain, page)
    azure_tc.track_metric(
        "sitemap-ad-listings-found", len(ad_listing_urls), properties={"domain": domain}
    )
    logging.info("Found %s ad_listings on %s", len(ad_listing_urls), message["domain"])
    if ad_listing_urls:
        new_ad_listings = TABLE.batch_merge_ad_listings(
            ad_listing_urls, message["domain"], message["metadata"]
        )
        logging.info(
            "Found %s new ad_listings on %s", new_ad_listings, message["domain"]
        )
        azure_tc.track_metric(
            "sitemap-new-ad-listings-found",
            new_ad_listings,
            properties={"domain": domain},
        )

    azure_tc.flush()
