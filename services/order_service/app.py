from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/orders")
def orders():
    # Simulate latency
    delay = random.uniform(0.1, 1.5)
    time.sleep(delay)

    # Simulate failure (20%)
    if random.random() < 0.2:
        return jsonify({"error": "Service failure"}), 500
    
    return {
        "orders": ["item1", "item2"],
        "latency": delay
    }
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)