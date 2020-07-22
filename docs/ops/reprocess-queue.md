# How to Reprocess Deadletters for a Particular Queue

Sometimes you fix an issue with the crawlers and then you want to take all the deadletters and reprocess them to make sure your fix results in more successes.

First, choose the queue you want to target. Here's [a list of the existing queues](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.ServiceBus/namespaces/pi-crawl/queues).

## Running the script from your machine

To run the script locally, you'll need to open `reprocess_dead_letter.py` and replace:
```
os.environ["SB_CONN_STR"]
```
with [the value configured here](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.Web/sites/pi-crawling/configuration).

Now run the following script:
```
// Change the queue argument to whichever queue you want to target
python3 tools/queues/reprocess_dead_letter.py "siteparse"
```

You may have to run it a few times to get everything back from deadletter to active for the queue.
In the queue details in Azure you should confirm everything is moved over.
