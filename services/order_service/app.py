# Import Flask framework to build web APIs
from flask import Flask, jsonify

# Import random to simulate unpredictable behavior (like real systems)
import random

# Import time to simulate latency (delay in response)
import time

# Import request to call another microservice (user-service)
import requests

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

# Create a Flask application instance
# __name__ tells Flask where to look for files/resources
app = Flask(__name__)

# Automatically traces all Flask routes
FlaskInstrumentor().instrument_app(app)

# -----------------------------------
# HEALTH CHECK ENDPOINT
# -----------------------------------
# This endpoint is used by monitoring systems to check if service is alive
@app.route("/health")
def health():
    # Return a simple JSON response
    return {"status": "ok"}

# ------------------------------------
# ORDERS ENDPOINT
# ------------------------------------
# This simulate a real backend API
@app.route("/orders")
def orders():
    # Create a custom trace span
    with tracer.start_as_current_span("order-processing"):

        # Simulate  random latency between 0.1s to 1.5s
        # In real systems, latency varies due to DB calls, network, etc.
        delay = random.uniform(0.1, 1.5)

        # Pause execution to simulate delay
        time.sleep(delay)

        # Simulate failure in 20% of requests
        # This helps test monitoring and alerting systems (SRE Concept)
        if random.random() < 0.2:
            return jsonify({"error": "Service failure"}), 500
    
        # Try calling user-service to get user data
        try:
            # Send HTTP GET request to user-service
            user_response = requests.get("http://localhost:5001/users")

            # Convert response JSON into Python dictionary
            user_data = user_response.json()

        except Exception as e:
            # If user-service is down, handle gracefully
            user_data = {"error": "User service unavailable"}

        # Return combined response
        return {
            "orders": ["item1", "item2"], # Sample order data
            "users": user_data, # Data from another service
            "latency": delay # Include latency for observability
        }

# -----------------------------
# APPLICATION ENTRY POINT
# -----------------------------
# This ensures that the app runs only when executed directly
if __name__ == "__main__":
    # Run Flask server
    # host="0.0.0.0" makes it accessible externally (important for Docker later)
    # port=5000 defines the port for this service
    app.run(host="0.0.0.0", port=5000)