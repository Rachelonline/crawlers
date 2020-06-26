# Siteloader

This function is used to load sitemapping jobs onto the sitemapping queue. It's configured to run once a day.

## How it works:

It's fairly simple in `siteloader.py` the `sitemapping_jobs()` returns a list of dicts which have the `domain` to sitemap and `metadata`.

The `SITES_TO_MAP` define which domains and metadata to sitemap.

## Adding a new site:

Add a new tuple to `SITES_TO_MAP` for the domain and the metadata dictionary.

## Removing a site to sitemap:

Remove the tuple from `SITES_TO_MAP`

*NOTE:* Because this is part of the sitemapping stage - if you want to stop crawling a site completely you'll need to also to disable the ad listing urls.

## Testing:

`pytest`

## Runbook:

This is triggered from a timer and loads into the sitemapping queue - there's not really all that much can go wrong. :)
