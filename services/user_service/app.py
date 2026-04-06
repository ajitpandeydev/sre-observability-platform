# Import Flask to create API service
from flask import Flask, jsonify

# Import random and time to simulate real-world latency
import random
import time

# ------------------------------------
# OpenTelemetry Setup (Tracing)
# ------------------------------------

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Create tracer provider (core tracing engine)
trace.set_tracer_provider(TracerProvider())

# Create exporter (prints traces to console for now)
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())

# Add processor to tracer
trace.get_tracer_provider().add_span_processor(span_processor)

# Get tracer instance (used to create spans)
tracer = trace.get_tracer(__name__)

# Create Flask app instance
app = Flask(__name__)

# -----------------------------------
# USER ENDPOINT
# -----------------------------------
@app.route("/users")
def users():
    with tracer.start_as_current_span("user-processing"):

        # Simulate small delay (faster than order service)
        delay = random.uniform(0.05, 0.8)

        # Pause execution to mimic processing time
        time.sleep(delay)

        # Return user data
        return {
            "users": ["Ajit", "Asmita", "Ojaswi"],
            "latency": delay
        }

# ----------------------------------------
# HEALTH CHECK ENDPOINT
# ----------------------------------------
@app.route("/health")
def health():
    return {"status": "ok"}

# ---------------------------------------
# APPLICATION ENTRY POINT
# ---------------------------------------
if __name__ == "__main__":
    # Run service on different port to avoid conflict 
    app.run(host="0.0.0.0", port=5001)