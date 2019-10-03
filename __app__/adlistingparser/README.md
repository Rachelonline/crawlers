# Ad listing crawler

This is crawler that gathers the contents of ad listing urls and passes them on to the parsing queue. It takes the url from the ad listings queue and loads the contents of the ad listings on the ad listing parse queue.

## How it works

`adlistingcrawler.py` does a get then puts the results on the next queue along with the ad-listing-crawled datetime to the metadata.

## Testing

`pytest`

## Runbook

TBD

