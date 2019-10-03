# Ad crawler

This is crawler that gathers the contents of ads and passes them on to the parsing queue. It takes the url from the ad queue and loads the contents of the ad on the ad parse queue.

## How it works

`adcrawler.py` does a get then puts the results on the next queue along with the ad-crawled datetime to the metadata.

## Testing

`pytest`

## Runbook

TBD

