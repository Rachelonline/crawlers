# crawlers!

This repo covers the crawlers - specifically the code that actually goes out on the web and fetches data. 

## Overview

Crawling is broken up into 3 different problems:
1. Collecting ads
2. Gathering ad listings (so we can get ads)
3. Mapping a site to get urls where ads are listed 

Because we want reliable and highly scaleable systems we use a queue based architecture. We've broken the problem down into several sub-apps inside this repo:
* siteloader - loads domains into the site mapping crawl queue 
* sitemapper - fetches the page we can parse out the ad listings from
* adlistings - gathers pages with ad listings. Those pages are parsed to gather ad urls
* ads - gathers ad pages. 

All of the parsing is done by a separate app function. These crawlers only collect and add jobs to downstream parse queues. 

One final thing to note - these jobs pass a 'metadata' dictionary along each step. This is used to provide context. (For example, what domain the job came from)

It's also good to review [Azure Functions Python guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)

## Siteloader

The siteloader is a timer based function that outputs jobs on the sitemappercrawling queue. 

More details here

## Sitemapper

The sitemapper gathers a page where we can gather the ad listings urls. 

It takes jobs from the sitemappercrawling queue and outputs jobs onto the sitemappingparser queue.

More details here

