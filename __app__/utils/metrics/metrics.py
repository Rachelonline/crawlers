import os
from applicationinsights import TelemetryClient
from applicationinsights.logging import enable
from applicationinsights.channel import (
    AsynchronousSender,
    AsynchronousQueue,
    TelemetryChannel,
)

AZURE_METRIC_KEY = os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")


def get_client():
    channel = TelemetryChannel(queue=AsynchronousQueue(AsynchronousSender()))
    return TelemetryClient(AZURE_METRIC_KEY, telemetry_channel=channel)


def enable_logging():
    enable(AZURE_METRIC_KEY)
