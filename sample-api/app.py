"""
Sample API Service
This is the main API that performs model inference.
It integrates with the preprocessing-service before prediction.

The original file was identical to the preprocessing-service, so the code below is the modified version
to work properly with the Pathway AI Challenge request according to my understanding.
"""

from flask import Flask, request, jsonify
import logging
from datetime import datetime
import os
import time
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# FIXED __name__ USAGE
# The original file had **name** and that would break the app
logger = logging.getLogger(__name__)
app = Flask(__name__)

SERVICE_VERSION = "1.0.0"
MODEL_VERSION = "1.0.0"

# ADDED ENV VARIABLE SUPPORT
# Keep default URL for docker-compose integration with preprocessing-service
# but allow override if needed in other environments
PREPROCESS_URL = os.environ.get(
    "PREPROCESS_URL",
    "http://preprocessing-service:5001/preprocess"
)

request_count = 0


# ADDED LOCAL FALLBACK PREPROCESSING
# This was added so the API can still work even if preprocessing-service is down
# also helps local tests not fail just because the external service is unavailable
def local_preprocess(text: str) -> str:
    return " ".join(text.strip().lower().split())


# ADDED INTEGRATION WITH PREPROCESSING SERVICE
# This is the main point of the challenge integration between services
# if the external service fails, fallback to local preprocessing instead of breaking everything
def call_preprocessing_service(text: str) -> str:
    try:
        response = requests.post(
            PREPROCESS_URL,
            json={"text": text, "operations": ["clean", "normalize"]},
            timeout=2
        )
        response.raise_for_status()
        data = response.json()

        # ADDED FLEXIBILITY
        # accept different possible field names in case preprocessing-service returns different structure
        if "processed_text" in data:
            return data["processed_text"]
        if "cleaned_text" in data:
            return data["cleaned_text"]
        if "text" in data:
            return data["text"]

        logger.warning("Preprocessing response missing expected fields. Using local fallback.")
        return local_preprocess(text)

    except Exception as exc:
        logger.warning("Preprocessing service unavailable. Using local fallback. Error: %s", exc)
        return local_preprocess(text)


# ADDED DUMMY MODEL LOGIC
# The challenge only needs a basic inference example, so this keeps it simple
# and enough to demonstrate the endpoint behavior
def predict_sentiment(text: str) -> dict:
    positive_words = {"good", "great", "excellent", "amazing", "love", "nice", "happy"}
    negative_words = {"bad", "terrible", "awful", "hate", "poor", "sad", "worst"}

    words = set(text.split())
    positive_score = len(words & positive_words)
    negative_score = len(words & negative_words)

    if positive_score > negative_score:
        sentiment = "positive"
        confidence = 0.92
    elif negative_score > positive_score:
        sentiment = "negative"
        confidence = 0.91
    else:
        sentiment = "neutral"
        confidence = 0.75

    return {
        "sentiment": sentiment,
        "confidence": confidence
    }


@app.route("/health", methods=["GET"])
def health_check():
    # KEEP HEALTH ENDPOINT FOR CONTAINER/K8S CHECKS
    return jsonify({
        "status": "healthy",
        "version": SERVICE_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.route("/ready", methods=["GET"])
def readiness_check():
    # KEEP READINESS ENDPOINT
    return jsonify({
        "status": "ready"
    }), 200


@app.route("/metrics", methods=["GET"])
def metrics():
    # FIXED METRICS RESPONSE
    # Added model_version because the tests expect this field
    return jsonify({
        "total_requests": request_count,
        "model_version": MODEL_VERSION,
        "service_version": SERVICE_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    """
    Main prediction endpoint.
    Steps:
    1. Receive raw text
    2. Send to preprocessing-service
    3. Receive cleaned text
    4. Run dummy model inference
    """
    global request_count
    request_count += 1

    start_time = time.time()

    # ADDED VALIDATION
    # prevent invalid content-type from being accepted
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    payload = request.get_json(silent=True)

    # ADDED VALIDATION
    # test file expects error when text field is missing
    if not payload or "text" not in payload:
        return jsonify({"error": "Missing required field: text"}), 400

    text = payload.get("text", "")

    # ADDED VALIDATION
    # test file also expects error for empty text
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Field 'text' must be a non-empty string"}), 400

    processed_text = call_preprocessing_service(text)
    prediction = predict_sentiment(processed_text)

    processing_time = round(time.time() - start_time, 6)

    return jsonify({
        "input_text": text,
        "processed_text": processed_text,
        "prediction": prediction,
        "model_version": MODEL_VERSION,
        "processing_time_seconds": processing_time
    }), 200


@app.route("/batch-predict", methods=["POST"])
def batch_predict():
    """
    Batch prediction endpoint.
    Expects JSON with 'texts' array.
    """
    global request_count
    request_count += 1

    start_time = time.time()

    # ADDED BATCH ENDPOINT
    # The uploaded tests expect /batch-predict but the original file did not really implement it
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    payload = request.get_json(silent=True)

    if not payload or "texts" not in payload:
        return jsonify({"error": "Missing required field: texts"}), 400

    texts = payload.get("texts")

    if not isinstance(texts, list) or len(texts) == 0:
        return jsonify({"error": "Field 'texts' must be a non-empty list"}), 400

    predictions = []

    for index, text in enumerate(texts):
        # ADDED PER-ITEM VALIDATION
        # keep batch processing running even if one item is invalid
        if not isinstance(text, str) or not text.strip():
            predictions.append({
                "index": index,
                "error": "Invalid text input"
            })
            continue

        processed_text = call_preprocessing_service(text)
        prediction = predict_sentiment(processed_text)

        predictions.append({
            "index": index,
            "input_text": text,
            "processed_text": processed_text,
            "prediction": prediction
        })

    processing_time = round(time.time() - start_time, 6)

    return jsonify({
        "predictions": predictions,
        "model_version": MODEL_VERSION,
        "processing_time_seconds": processing_time
    }), 200


@app.route("/", methods=["GET"])
def root():
    # KEEP ROOT ENDPOINT FOR QUICK SERVICE INFO
    return jsonify({
        "service": "Sample API",
        "version": SERVICE_VERSION,
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "metrics": "/metrics",
            "predict": "/predict (POST)",
            "batch_predict": "/batch-predict (POST)"
        }
    }), 200


if __name__ == "__main__":
    # FIXED STARTUP SECTION
    # The original file had broken __name__ usage and incomplete logger/app.run lines
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"

    logger.info("Starting Sample API on port %s", port)
    app.run(host="0.0.0.0", port=port, debug=debug)