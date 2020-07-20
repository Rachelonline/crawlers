# Monitoring

This provides a basic monitoring service which checks the number of new ads found in the last 24 hours and posts the results to the #tech-alerting-and-monitoring slack channel.

It uses slack webhook and a basic POST to slack.

This was thrown together pretty quickly so it could be improved 🙂

## Developing locally:

Get the `APP_INSIGHTS_KEY`, `APP_INSIGHT_ID`, and `SLACK_KEY` from keybase. Save them in your local.settings.json.

The entire function lives in `__init__.py` and can be run locally with

```bash
python3 __app__/monitoring/__init__.py
```
