from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

@app.route("/users")
def users():
    delay = random.uniform(0.05, 0.8)
    time.sleep(delay)

    return {
        "users": ["Ajit", "Asmita", "Ojaswi"],
        "latency": delay
    }

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)