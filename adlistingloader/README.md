# Ad listing Loader

This function loads individual ad listing urls onto the ad listing crawl queue. It's configured to run once an hour.

## How it works

`adlistingloader.py` isn't very deep - the real interesting parts are in `utils/table/adlisting.py`.

Basically it filters the ad listing urls to ones that are flagged as enabled (the default) and returns a job of the url and metadata.

## Adding a new ad listing url

Generally you shouldn't be doing this manually - the site map parsers add new ad listing urls automatically.

You can do it manually by adding a new row to the `adlistings` table, but be sure to get the metadata along with it.

## Enabling/Disabling an ad listing url

New ad listing urls are enabled by default. To disable them set the `enabled` property to `false` in the azure table. 

You might want to do this to avoid crawling regions we don't care about - such as ones located outside the US and Canada.

## Testing:

`pytest`

## Runbook

TBD
