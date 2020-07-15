import os
import json
from collections import defaultdict
import azure.functions as func
import requests


def get_metric(metric_name):
    """ Gets the custom metric from app insights """
    url = f"https://api.applicationinsights.io/v1/apps/{os.environ['APP_INSIGHT_ID']}/metrics/customMetrics%2F{metric_name}"
    params = {
        "timespan": "P1D",
        "interval": "P1D",
        "aggregation": "sum",
        "segment": "customDimensions/domain",
        "top": 50,
    }
    headers = {"x-api-key": os.environ["APP_INSIGHTS_KEY"]}
    r = requests.get(url, params=params, headers=headers)
    return r.json()


def process_data(metric_name: str, raw_data: dict) -> dict:
    """
    Changes the raw data into a per domain/metric dictinary. Will combine
    any cross day boundries
    """
    domain_metrics = defaultdict(int)
    for day_values in raw_data["value"]["segments"]:
        for segment in day_values["segments"]:
            domain = segment["customDimensions/domain"]
            domain_metrics[domain] += segment[f"customMetrics/{metric_name}"].get("sum")

    return domain_metrics


def send_slack(message: dict) -> None:
    """ Sends to slack """
    hook_url = f"https://hooks.slack.com/services/{os.environ['SLACK_KEY']}"
    requests.post(hook_url, json=message)


def format_message(data: dict) -> dict:
    """ Creates a rich slack message structure """
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Here's the crawl metrics for the last 24 hours:",
                "verbatim": True,
            },
        }
    ]

    for domain, metrics in data.items():
        blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*{domain}:*", "verbatim": True},
            }
        )
        metrics_str = "\n".join(metrics)
        blocks.append(
            {"type": "section", "text": {"type": "mrkdwn", "text": f"{metrics_str}"}}
        )
    return {"blocks": blocks}


def main(timer: func.TimerRequest) -> None:
    metric_names = [
        "new-ads-found",
        "ad-crawl-success",
        "ad-parse-success",
        "ad-processed",
        "images-found",
        "image-crawl-success",
        "image-already-crawled",
    ]
    data = defaultdict(list)
    for metric_name in metric_names:
        raw_data = get_metric(metric_name)
        clean_data = process_data(metric_name, raw_data)
        for domain, values in clean_data.items():
            data[domain].append(f"{metric_name}: {values}")

    message = format_message(data)
    send_slack(message)


if __name__ == "__main__":
    main(None)
