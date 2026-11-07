from fastapi import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

# Define operational metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

JOB_FAILURE_COUNT = Counter(
    "background_job_failures_total", "Total background job failures", ["job_type"]
)


def metrics_view():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
