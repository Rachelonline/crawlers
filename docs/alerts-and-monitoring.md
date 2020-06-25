# Using Azure Monitor Alerts

You can set up alerts through Alert Rules in Azure Monitor, Application Insights, etc. that will automatically trigger certain behavior.

[Create an Azure Monitor alert from a log query](https://docs.microsoft.com/en-us/azure/azure-monitor/learn/tutorial-response) The term **Log Alert** describes alerts where a log query in [Log Analytics workspace](https://docs.microsoft.com/en-us/azure/azure-monitor/learn/tutorial-viewdata) or [Application Insights](https://docs.microsoft.com/en-us/azure/azure-monitor/app/analytics) is evaluated, and an alert fired if the result is true.

For example, you could set up Alert Rules on the [Crawling Azure CosmosDB](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.DocumentDb/databaseAccounts/crawling/overview) to activate behavior if the log includes an uptick in crawler failures.

1. Under Alerts on your resource of choice, add a new Alert Rule.
2. Choose your Condition for sending the Alert.
3. Choose or create an Action Group.

4. Attach to a [Webhook](https://azure.microsoft.com/en-us/blog/webhooks-for-azure-alerts/) to route alerts as JSON to an HTTP endpoint, e.g. [Slack](https://api.slack.com/messaging/webhooks#posting_with_webhooks).
   1. Optionally, [set up a Logic app](https://github.com/Azure/azure-quickstart-templates/tree/master/201-alert-to-slack-with-logic-app) to handle the webhook.

#### Where do I attach my Alert?

There's a lot of different places you can create Alert Rules. The main options are going to be *on* the service you're looking to track or on a service analyzing its results, like Application Insights. The second option allows you to be more granular in terms of troubleshooting data, since you'll be working with generated insights, whereas the first has you working more directly with the resource's metrics.

# Using Azure Logic Apps

[Azure Logic App documentation](https://docs.microsoft.com/en-us/azure/logic-apps/)

Essentially, Logic Apps are a visual code workflow creator that allows you to connect different behavior based on a trigger. For example, you can receive an HTTP request and send a message using the body, or you can run a query on a schedule. They're pretty easy to set up, and there are a number of Templates available for Logic Apps in the documentation that let you plug-and-play.

## Apps with an External Trigger

As mentioned, Logic Apps can be run from an external trigger like an HTTP request, then use the values sent to run other functions.

### Slack-Messaging-App: Azure Alerts Through Logic

[Alert to Slack with Logic App template](https://azure.microsoft.com/en-us/resources/templates/201-alert-to-slack-with-logic-app/)

At the time of this writing, the Logic App [Slack-Messaging-App](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.Logic/workflows/Slack-Messaging-App/logicApp) is used to relay an HTTP request with a Body that conforms to the [common Azure Monitor alert schema](https://docs.microsoft.com/en-us/azure/azure-monitor/platform/alerts-common-schema) to the Slack channel #tech-alerting-and-monitoring.

#### Adding a New Alert to Slack-Messaging-App

If you want to relay another alert through the Slack-Messaging-App, do the following:

1. [Create an alert rule](https://docs.microsoft.com/en-us/azure/azure-monitor/platform/alerts-overview#create-an-alert-rule) in Azure Monitor for the service you're testing.
2. Under *Action group*, select the action group *Tech Slack Alerts*.
3. Give your alert rule readable and descriptive details - the name, description, and severity will all be relayed through Slack.

Slack-Messaging-App should do all the handling of the body, but if your alerts are coming through with the rule name, description, and severity but *not* any details (i.e. with message text including 'Additional context not provided'), then the specific alert schema you're using is not yet supported by Slack-Messaging-App.

​	*Note: Make sure any [action group you set up](https://docs.microsoft.com/en-us/azure/azure-monitor/platform/action-groups) to send to Slack-Messaging-App USES the Common Alert 		Schema, or the Logic App will not recognize input.*

#### Extending Slack-Messaging-App to New Incoming Schemas

At the time of this writing, Slack-Messaging-App is [integrated with the common alert schema](https://docs.microsoft.com/en-us/azure/azure-monitor/platform/alerts-common-schema-integrations) where `MonitoringService == 'Platform'`. This allows the Logic app to reference an additional AlertContext field in the HTTP request, such as the metric being measured by the alert, its value, etc. If the external trigger sending your HTTP request includes fields outside of the common alert schema you want to reference, you'll have to set up another conditional inside Slack-Messaging-App like the one that already exists and is seen below:

![image-20200625091229239](C:\Users\Lucy\AppData\Roaming\Typora\typora-user-images\image-20200625091229239.png)

When you've added a new conditional, make sure previous ones still run and relay other kinds of alerts successfully. There should be a disabled Alert rule in *pi-crawling Application Insights>Alerts* called *Dummy Alert for Slack* you can use to test Azure alert handling with Slack-Messaging-App - it sends alerts every minute, though, so be sure to disable it once you're done!

## Apps on a Schedule

#### Setting up with a Recurring Trigger

[Schedule Recurring jobs through Logic](https://docs.microsoft.com/en-us/azure/scheduler/migrate-from-scheduler-to-logic-apps#schedule-recurring-jobs)

#### Setting up with TimerJobs

I haven't done this, just something I saw a lot of documentation for.

[Schedule tasks and processes with Logic](https://docs.microsoft.com/en-us/azure/logic-apps/concepts-schedule-automated-recurring-tasks-workflows)

[Execute timer jobs through a Logic App template](https://github.com/Azure/azure-quickstart-templates/tree/master/301-logicapps-jobscheduler/) *Note: This creates an instance of a TimerJob through a Logic App to avoid running into 'workflow limits.'*

### Why Not Azure Timer Functions?

Previously, the Crawling Rollup was run through a *monitoring* function in *pi-crawling>Functions* that ran on a specified schedule and called a Python script to query from Application Insights, then message Slack. That's an absolutely valid way to schedule a process, and may [be better suited for some scenarios](https://www.serverless360.com/blog/when-to-use-logic-apps-and-azure-functions).

Basically, though, Logic is more easily extensible and configurable, and there's less overhead involved connecting it to metrics not tracked in Application Insights, such as deadletter queue length in Azure Service Bus. *(Previously, the Python script required local devs to find/store a number of different keys for every service whose metrics they wanted to access.)*

##### Querying Custom Metrics from the Backend

Here's the code that was used in `__init__.py` , combined with a list of custom metric names like *new-ads-found*. The custom metrics names are in *Application Insights>Logs>customMetrics* or *Application Insights>Metrics*.

```
  url = f"https://api.applicationinsights.io/v1/apps/{os.environ['APP_INSIGHT_ID']}/metrics/customMetrics%2F{metric_name}"

  params = {

​    "timespan": "P1D",

​    "interval": "P1D",

​    "aggregation": "sum",

​    "segment": "customDimensions/domain",

​    "top": 50,

  }

  headers = {"x-api-key": os.environ["APP_INSIGHTS_KEY"]}

  r = requests.get(url, params=params, headers=headers)
```

### Scheduled-Crawling-Rollup: Azure Logs to Slack Through Logic

[Logic Azure Monitor Logs connector](https://docs.microsoft.com/en-us/azure/azure-monitor/platform/logicapp-flow-connector) *At the time of this writing, apparently this connector replaces the Application Insights connector.*

[Azure Service Bus connector](https://docs.microsoft.com/en-us/azure/connectors/connectors-create-api-servicebus) *See other connector docs in the sidebar. This is for modifying queues; use Monitor Logs connector to query metrics.*

The Crawler Rollup is a scheduled process that runs every day at 6:30pm GMT; queries metrics from *pi-crawling* Application Insights, as well as services that[ stream their custom metrics](https://docs.microsoft.com/en-us/azure/azure-monitor/platform/diagnostic-settings) to a Log Analytics workspace; then sends those messages to the #tech-alerting-and-monitoring Slack Channel through a Logic Workflow connector.

#### Querying with the Azure Monitor Logs Connector

Currently, the Azure Monitor Logs connector in Scheduled-Crawling-Rollup is set to [run a query and list results](https://docs.microsoft.com/en-us/connectors/azuremonitorlogs/#run-query-and-list-results), which are then processed for Slack messages. There is also an option to visualize query results.

Queries through Azure Monitor Logs - whether to Application Insights, or to the Log Analytics Workspace where other services' metrics are streamed - are written in [Kusto query language](https://docs.microsoft.com/en-us/azure/kusto/query).

To find examples of queries and test them out, see [Example queries for pi-crawling | Logs](https://portal.azure.com/#@seattleagainstslavery.org/resource/subscriptions/eb3b9f64-5569-4792-90ad-7c5a3954c142/resourceGroups/crawling/providers/Microsoft.Web/sites/pi-crawling/appInsightsQueryLogs). Specifically look at *Queries>Application Insights* in the sidebar. This page allows you to create a New Queries for *pi-crawling Application Insights*, see the associated code, and run the query for sample data.

When you've decided on your query, just copy that code and paste it into the *Query* field of your connector.

​	Note: You can either set the timestamp in your query, or with the Time Range field just below, which is a tiny bit more readable.

##### Queries for Custom Metrics

Metrics like *adcrawler Successes* are [log-based Metrics](https://docs.microsoft.com/en-us/azure/azure-monitor/app/pre-aggregated-metrics-log-metrics#log-based-metrics) generated by Application Insights. To find the query code for them, you can go to *Metrics* under Application Insights, add a query to the chart with the filter you'd like - for example, getting the Sum of *new-ads-found* - and then look at the Logs for it.

![image-20200625105734269](C:\Users\Lucy\AppData\Roaming\Typora\typora-user-images\image-20200625105734269.png)

In this example, the Recommended Log for new-ads-found in the last day is:

```
customMetrics
| where timestamp >= ago(1d)
| where name == "new-ads-found"
| extend customMetric_valueSum = iif(itemType == 'customMetric',valueSum,todouble(''))
| summarize ['customMetrics/new-ads-found_sum'] = sum(customMetric_valueSum) by bin(timestamp,1h)
| order by timestamp desc
```

Generally, you can query Custom Metrics under *Application insights>customMetrics* on the Logs tab.

#### Adding a Metric to the Rollup

Set up additional steps in the Logic App to query through Azure Monitor Log - or whatever connector is relevant - and parse the output for messaging with another step.

#### Adding a New Rollup Subscriber

If you want to add a new channel, user, etc. to the Crawler Rollup, such as an email subscription, you can add a new connector to the Logic workflow alongside the Slack connector.

