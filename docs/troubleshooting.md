# Troubleshooting

[A list of Azure Resources related to Crawling](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/overview)

[Look at logs for pi-crawling App Service](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.Web/sites/pi-crawling/appInsightsQueryLogs)

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

[Crawling Azure Cosmos DB](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.DocumentDb/databaseAccounts/crawling/overview)
In the `Overview` section there is a decent graph of requests in the past little while (1 hour to 30 days).
Definitely poke around in the `Data Explorer`. Look in the `crawling > ads > Items` section. Edit the filter to be:
```
ORDER BY c._ts DESC
```
By looking at the first record returned when that query is run will tell you the last time the crawling of a page was successfully done.

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

If you want to see how the Service Bus is doing use [pi-crawl's Service Bus Explorer](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.ServiceBus/namespaces/pi-crawl/queues)

Look at `Queues`.
Select each one and make sure it is not out of space. If it is, click on `Properties` and increase the `Maximum Size` then `Save Changes`.

If you'd like to actually see what is in one of the queues, use the `Service Bus Explorer's` `Peek` option.

Queue vs Deadletter
Queue is what is in the queue.
Deadletter was kicked out of the queue (most likely because it tried and failed to process a few times)
Once you select `Peek` you can click on records to see more details.

Look into recent changes to the crawlers. (not currently autodeploying but master is generally current)
https://github.com/seattleagainstslavery/crawlers/commits/master

[Stop Crawling a Domain](./ops/disable-site.md)
