# ------------------------------------
# USER SERVICE - OBSERVABILITY ENABLED
# ------------------------------------

from flask import Flask, jsonify
import random
import time

# ------------------------------------
# Prometheus Metrics
# ------------------------------------
from prometheus_client import Counter, Histogram, start_http_server

USER_REQUEST_COUNT = Counter(
    'user_requests_total',
    'Total number of user requests'
)

USER_LATENCY = Histogram(
    'user_request_latency_seconds',
    'Latency of user requests'
)

# ------------------------------------
# OpenTelemetry Setup (Tracing)
# ------------------------------------
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Configure tracer provider
provider = TracerProvider()
trace.set_tracer_provider(provider)

# Export traces to OTEL Collector
span_processor = SimpleSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(span_processor)

# Get tracer instance
tracer = trace.get_tracer(__name__)

# ------------------------------------
# Flask App Setup
# ------------------------------------
app = Flask(__name__)

# Auto-instrument Flask
FlaskInstrumentor().instrument_app(app)

# ------------------------------------
# USER ENDPOINT
# ------------------------------------
@app.route("/users")
def users():
    USER_REQUEST_COUNT.inc()

    with USER_LATENCY.time():
        with tracer.start_as_current_span("user-processing"):

            delay = random.uniform(0.05, 0.8)
            time.sleep(delay)

            return {
                "users": ["Ajit", "Asmita", "Ojaswi"],
                "latency": delay
            }

# ------------------------------------
# HEALTH CHECK ENDPOINT
# ------------------------------------
@app.route("/health")
def health():
    return {"status": "ok"}

# ------------------------------------
# APPLICATION ENTRY POINT
# ------------------------------------
if __name__ == "__main__":
    print("Starting Prometheus metrics server on port 8000...")
    start_http_server(8000)

    print("Starting User Service on port 5001...")
    app.run(host="0.0.0.0", port=5001)