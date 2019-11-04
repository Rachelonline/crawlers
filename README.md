# Crawlers

## TOC:

- Getting started
- Runbook
- High Level Design
- Crawler Design
- Rough Edges

## High level crawling process

Gathering data from the across the web is a dynamic and continually evolving challenge.

To make things manageable the problem is broken up into 4 different stages:

1. Collecting sitemaps
2. Crawling ad listings
3. Crawling individual ads
4. Processing ad data and crawling ad images

Each stage of the process feeds into the next.

A sitemap is a collection of all the ad listing urls on a page. This is generally slow changing so we only check for new listings once per day.

Ad listings are pages that list links to individual ads. We depth crawl those once an hour to get new ads to crawl. Depth crawling means we will crawl ad listings, find the url for the "next" ad listings then crawl the new ad listing url. We continue the process of crawling ad listings, gather ads, then find the next set of ads until we hit a max depth or until we've already crawled "enough" ads on the page. Think of this as going back in time on sites like craigslist.

Once we have the individual ad urls we then crawl those ads. Raw ads are saved in blobstore and structured ad data is sent to the processing step.

In the final processing step we ad the structured ad data into CosmosDB and save ad images to blobstore.

To be good web citizens we also have a per-domain shared throttle so we will limit the rate which we crawl any website.

Crawling is broken up into 3 different problems:

1. Collecting ads
2. Gathering ad listings (so we can get ads)
3. Mapping a site to get ad listing urls

Because we want reliable and highly scaleable systems we use a queue based architecture. We've broken the problem down into several sub-apps inside this repo:

- siteloader - loads domains into the site mapping crawl queue
- sitemapper - fetches the page we can parse out the ad listings from
- adlistings - gathers pages with ad listings. Those pages are parsed to gather ad urls
- ads - gathers ad pages.

All of the parsing is done by a separate app function. These crawlers only collect and add jobs to downstream parse queues.

One final thing to note - these jobs pass a 'metadata' dictionary along each step. This is used to provide context. (For example, what domain the job came from)

It's also good to review [Azure Functions Python guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)

## General:

Functions are split into the `__init__.py` and `main.py` functions. The `__init__.py` handles pulling/putting messages on queues and passing the message to the `main.py` function.

You don't super need to test the `__init__.py` but be sure the `main.py` is well covered.

There's also a `utils/` folder for some common code (mostly networking).

## General crawl issues:

`TODO: docs on this`

## Setting up local dev

Set up the Azure core tools [locally](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#brew)

For Macs:

1. Ensure you have virtualenvs set up following [this guide](https://sourabhbajaj.com/mac-setup/Python/virtualenv.html).
2. Install Azure Function Core Tools:

```
brew tap azure/functions
brew install azure-functions-core-tools
```

3. Intstall local requirements: `python -m pip install -r __app__/requirements.txt`

You'll also need to get the connection strings so you can get the right queues. (check with [Liz](liz@seattleagainstslavery.org) for that)

`#TODO: Windows install instructions`

## Siteloader

The siteloader is a timer based function that outputs jobs on the sitemappercrawling queue.

More details here

## Sitemapper

The sitemapper gathers a page where we can gather the ad listings urls.

It takes jobs from the sitemappercrawling queue and outputs jobs onto the sitemappingparser queue.

More details here
