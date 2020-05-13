import logging
from __app__.utils.table.adlisting import AdListingTable
from __app__.sitemapparser.sites.cityxguide_com import cityxguide_com
from __app__.sitemapparser.sites.cityxguide_net import cityxguide_net
from __app__.sitemapparser.sites.capleasures_com import capleasures_com
from __app__.sitemapparser.sites.escortdirectory import escortdirectory
from __app__.sitemapparser.sites.vipgirlfriend_com import vipgirlfriend_com
from __app__.sitemapparser.sites.megapersonals_eu import megapersonals_eu
from __app__.sitemapparser.sites.onebackpage_com import onebackpage_com
from __app__.sitemapparser.sites.twobackpage_com import twobackpage_com
from __app__.utils.metrics.metrics import get_client, enable_logging


SITE_PARSERS = {
    "cityxguide.com": cityxguide_com,
    "cityxguide.net": cityxguide_net,
    "capleasures.com": capleasures_com,
    "escortdirectory.com": escortdirectory,
    "vipgirlfriend.com": vipgirlfriend_com,
    "megapersonals.eu": megapersonals_eu,
    "2backpage.com": twobackpage_com,
    "onebackpage.com": onebackpage_com,
}

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
