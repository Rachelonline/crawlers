# How to Stop Crawling a Domain

## Temporary disable a domain:

When you want to just disable the crawling of a domain you can use `tools/adlistings/stop_crawling_domain.py`. It will disable the aslistings from being loaded as part of the hourly crawl. This will then prevent the downstream ad crawling and image crawling.

First replace environmental constants locally.
From [pi-crawling App Service Configuration](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.Web/sites/pi-crawling/configuration) you'll need `SB_CONN_STR` and `TABLE_SERVICE_KEY`.

Locally (don't commit them to the Git repository!), you need to put those strings into `stop_crawling_domain.py`.

```
python3 tools/adlistings/stop_crawling_domain.py "onebackpage.com"
```

It will also go through the existing adlistingcrawl queue and remove any crawl jobs for that domain.

This is a soft delete, you can re-enable the domain in the table and it will start crawling again.

**manual step** you'll also need to disable the `SITEMAP_URL` in the site-loader and deploy. This is a less critical step, but you'll still need to do it.

## Permanently disable a domain:

First temporary disable, then delete the code.
