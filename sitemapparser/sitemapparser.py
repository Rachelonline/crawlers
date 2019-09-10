import logging
from utils.table.adlisting import AdListingTable
from sitemapparser.sites.cityxguide_com import cityxguide_com


SITE_PARSERS = {"cityxguide.com": cityxguide_com}

TABLE = AdListingTable()


def parse_ad_listing_page(domain, page):
    parser = SITE_PARSERS.get(domain)
    if parser is None:
        logging.error("No site map crawler for %s", domain)
        return None
    return parser(page)


def parse_sitemap(message):
    page = message["sitemapping-page"]
    domain = message["domain"]
    ad_listing_urls = parse_ad_listing_page(domain, page)
    logging.info("Found %s ad_listings on %s", len(ad_listing_urls), message["domain"])
    if ad_listing_urls:
        TABLE.batch_merge_ad_listings(
            ad_listing_urls, message["domain"], message["metadata"]
        )
