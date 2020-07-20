# Troubleshooting

[A list of Azure Resources related to Crawling](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/overview)

## [To get a quick look at what is happening in the pi-crawling App Service in real time or details of exceptions being thrown.](https://portal.azure.com/#blade/AppInsightsExtension/QuickPulseBladeV2/ComponentId/%7B%22Name%22%3A%22pi-crawling%22%2C%22SubscriptionId%22%3A%22eb3b9f64-5569-4792-90ad-7c5a3954c142%22%2C%22ResourceGroup%22%3A%22crawling%22%7D/ResourceId/%2Fsubscriptions%2Feb3b9f64-5569-4792-90ad-7c5a3954c142%2FresourceGroups%2Fcrawling%2Fproviders%2Fmicrosoft.insights%2Fcomponents%2Fpi-crawling)

## Looking at logs for pi-crawling App Service
[Link to logs where you can query](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.Web/sites/pi-crawling/appInsightsQueryLogs)

This query will tell you how many failures you have in a given time range. By shifting the time range around you should be able to see when a large number of failures began.
```
dependencies
| where success == false
| summarize totalCount=sum(itemCount) by type
| top 5 by totalCount desc
```

You can also run this query to look at a graph of the average time requests took:
```
requests
| where timestamp > ago(17d)
| summarize avgRequestDuration=avg(duration) by bin(timestamp, 4h) // use a time grain of your choice
| render timechart
```

If you want to see what operations are causing failures:
```
// You must manually choose the time range
requests
| where success == false
| summarize failedCount=sum(itemCount), impactedUsers=dcount(user_Id) by operation_Name
| order by failedCount desc
```

If you need to see what dependencies are failing the most:
```
dependencies
| where success == false
| summarize totalCount=sum(itemCount) by type
| top 5 by totalCount desc
```

## Looking in Cosmos (where the data ends up)
[Crawling Azure Cosmos DB](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.DocumentDb/databaseAccounts/crawling/overview)
In the `Overview` section there is a decent graph of requests in the past little while (1 hour to 30 days).
Definitely poke around in the `Data Explorer`. Look in the `crawling > ads > Items` section. Edit the filter to be:
```
ORDER BY c._ts DESC
```
By looking at the first record returned when that query is run will tell you the last time the crawling of a page was successfully done. `_ts` is created by Cosmos and shows the latest time the record was changed (created or updated).

If you are investigating a particular crawler you can run the same query with the domain specified:
```
// replace cityxguide.com with whatever crawler you are looking into
WHERE c.metadata.domain = "cityxguide.com" ORDER BY c._ts DESC
```

Do you need to know which records are after a certain time? (You may need a [unix time converter](http://www.onlineconversion.com/unix_time.htm))

```
// this is in unix time btw
WHERE c._ts > 1592179200
```

Want to see how many records have been added or updated since a certain time?
You must click on New SQL Query icon

```
SELECT VALUE COUNT(1) FROM c WHERE c._ts > 1594819755
```

## Looking at Service Bus Queues (they feed the serverless function)

### [To see metrics on a queue by queue basis](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.ServiceBus/namespaces/pi-crawl/metrics)

Select some metric ("Outgoing Messages" is a good choice).

Select "Apply Splitting"

In the Splitting Widget choose "EntityName" as the "Values"

The metrics now split out each queue into its own line on the graph.

To filter out everything else, Select "Add Filter" and only select the Queues you want to see.

### To see how full a Service Bus Queue is[pi-crawl's Service Bus Explorer](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.ServiceBus/namespaces/pi-crawl/queues)

Look at `Queues`.
Select each one and make sure it is not out of space. If it is, click on `Properties` and increase the `Maximum Size` then `Save Changes`.

If you'd like to actually see what is in one of the queues, use the `Service Bus Explorer's` `Peek` option.

### Queue vs Deadletter
Queue is what is in the queue.
Deadletter was kicked out of the queue (most likely because it tried and failed to process a few times)
Once you select `Peek` you can click on records to see more details.

If you see errors like "MaxDeliveryCountExceeded" with a message like this: "Message could not be consumed after 10 delivery attempts.", chances are high that something is broken in the functions. Use the link at the top of this document to inspect the exceptions coming through in real time.

## How to Remove All Messages From Queue When A Site Is Down

Only remove messages from crawling related queues. This is because they require connecting to the site that is down.

The following queues are ones that you'll need to clear out:
```
imagecrawl
pagecrawl
regioncrawl
sitecrawl
```

To remove all messages relying on example site "megapersonals.eu" run the following:
```
python3 tools/queues/remove_messages_from_queue.py "megapersonals.eu" "imagecrawl" "active"
python3 tools/queues/remove_messages_from_queue.py "megapersonals.eu" "imagecrawl" "deadletter"
python3 tools/queues/remove_messages_from_queue.py "megapersonals.eu" "pagecrawl" "active"
python3 tools/queues/remove_messages_from_queue.py "megapersonals.eu" "pagecrawl" "deadletter"
python3 tools/queues/remove_messages_from_queue.py "megapersonals.eu" "regioncrawl" "active"
python3 tools/queues/remove_messages_from_queue.py "megapersonals.eu" "regioncrawl" "deadletter"
python3 tools/queues/remove_messages_from_queue.py "megapersonals.eu" "sitecrawl" "active"
python3 tools/queues/remove_messages_from_queue.py "megapersonals.eu" "sitecrawl" "deadletter"
```

## [Need to Stop Crawling a Domain?](./ops/disable-site.md)

## [Need to Reprocess Records in Deadletter Queue?](./ops/reprocess-queue.md)
