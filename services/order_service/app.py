# ------------------------------------
# ORDER SERVICE - OBSERVABILITY ENABLED
# ------------------------------------

from flask import Flask, jsonify
import random
import time
import requests

# ------------------------------------
# OpenTelemetry Setup (Tracing)
# ------------------------------------
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Configure tracer provider
provider = TracerProvider()
trace.set_tracer_provider(provider)

# Export traces to OTEL Collector
span_processor = SimpleSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(span_processor)

# Get tracer instance
tracer = trace.get_tracer(__name__)

# ------------------------------------
# Prometheus Metrics
# ------------------------------------
from prometheus_client import Counter, Histogram, start_http_server

# Count total requests
REQUEST_COUNT = Counter(
    'order_requests_total',
    'Total number of order requests'
)

# Measure latency
REQUEST_LATENCY = Histogram(
    'order_requests_latency_seconds',
    'Latency of order requests'
)

# ------------------------------------
# Flask App Setup
# ------------------------------------
app = Flask(__name__)

# Auto-instrument Flask
FlaskInstrumentor().instrument_app(app)

# Auto-instrument outgoing HTTP calls
RequestsInstrumentor().instrument()

# ------------------------------------
# HEALTH CHECK ENDPOINT
# ------------------------------------
@app.route("/health")
def health():
    return {"status": "ok"}

# ------------------------------------
# ORDERS ENDPOINT
# ------------------------------------
@app.route("/orders")
def orders():
    REQUEST_COUNT.inc()

    with REQUEST_LATENCY.time():
        with tracer.start_as_current_span("order-processing"):

            # Simulate latency
            delay = random.uniform(0.1, 1.5)
            time.sleep(delay)

            # Simulate failure (20% chance)
            if random.random() < 0.2:
                return jsonify({"error": "Service failure"}), 500

            # Call user-service
            try:
                user_response = requests.get("http://localhost:5001/users")
                user_data = user_response.json()
            except Exception:
                user_data = {"error": "User service unavailable"}

            return {
                "orders": ["item1", "item2"],
                "users": user_data,
                "latency": delay
            }

# ------------------------------------
# APPLICATION ENTRY POINT
# ------------------------------------
if __name__ == "__main__":
    print("Starting Prometheus metrics server on port 8001...")
    start_http_server(8001)

    print("Starting Order Service on port 5000...")
    app.run(host="0.0.0.0", port=5000)