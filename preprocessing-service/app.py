"""
Data Preprocessing Service
This service handles data cleaning and transformation before model inference.
Candidates should containerize and integrate this with the main API.
"""

from flask import Flask, request, jsonify
import re
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

SERVICE_VERSION = "1.0.0"
request_count = 0


class TextPreprocessor:
    """Handles text preprocessing tasks"""
    
    @staticmethod
    def clean_text(text):
        """Basic text cleaning"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters (keeping basic punctuation)
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        # Strip leading/trailing whitespace
        text = text.strip()
        return text
    
    @staticmethod
    def normalize_text(text):
        """Normalize text to lowercase"""
        return text.lower()
    
    @staticmethod
    def remove_urls(text):
        """Remove URLs from text"""
        return re.sub(r'http\S+|www.\S+', '', text)
    
    @staticmethod
    def remove_emails(text):
        """Remove email addresses"""
        return re.sub(r'\S+@\S+', '', text)


preprocessor = TextPreprocessor()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "version": SERVICE_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.route('/ready', methods=['GET'])
def readiness_check():
    """Readiness check endpoint"""
    return jsonify({"status": "ready"}), 200


@app.route('/metrics', methods=['GET'])
def metrics():
    """Basic metrics endpoint"""
    return jsonify({
        "total_requests": request_count,
        "version": SERVICE_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.route('/preprocess', methods=['POST'])
def preprocess():
    """
    Preprocess text data.
    Expects JSON with:
    - text: string to preprocess
    - operations: list of operations to apply (optional)
    """
    global request_count
    request_count += 1
    
    try:
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({
                "error": "Missing required field: 'text'"
            }), 400
        
        text = data['text']
        operations = data.get('operations', ['clean', 'normalize'])
        
        logger.info(f"Processing text with operations: {operations}")
        
        # Apply requested operations
        processed_text = text
        
        if 'clean' in operations:
            processed_text = preprocessor.clean_text(processed_text)
        
        if 'normalize' in operations:
            processed_text = preprocessor.normalize_text(processed_text)
        
        if 'remove_urls' in operations:
            processed_text = preprocessor.remove_urls(processed_text)
        
        if 'remove_emails' in operations:
            processed_text = preprocessor.remove_emails(processed_text)
        
        response = {
            "original_text": text,
            "processed_text": processed_text,
            "operations_applied": operations,
            "original_length": len(text),
            "processed_length": len(processed_text),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route('/batch-preprocess', methods=['POST'])
def batch_preprocess():
    """
    Batch preprocessing endpoint.
    Expects JSON with 'texts' array.
    """
    global request_count
    request_count += 1
    
    try:
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        if 'texts' not in data:
            return jsonify({
                "error": "Missing required field: 'texts'"
            }), 400
        
        texts = data['texts']
        operations = data.get('operations', ['clean', 'normalize'])
        
        if not isinstance(texts, list):
            return jsonify({
                "error": "'texts' must be an array"
            }), 400
        
        processed_texts = []
        for text in texts:
            if isinstance(text, str):
                processed = text
                
                if 'clean' in operations:
                    processed = preprocessor.clean_text(processed)
                
                if 'normalize' in operations:
                    processed = preprocessor.normalize_text(processed)
                
                if 'remove_urls' in operations:
                    processed = preprocessor.remove_urls(processed)
                
                if 'remove_emails' in operations:
                    processed = preprocessor.remove_emails(processed)
                
                processed_texts.append(processed)
            else:
                processed_texts.append("")
        
        response = {
            "processed_texts": processed_texts,
            "count": len(processed_texts),
            "operations_applied": operations,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Batch processed {len(processed_texts)} texts")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing batch request: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with service information"""
    return jsonify({
        "service": "Data Preprocessing Service",
        "version": SERVICE_VERSION,
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "metrics": "/metrics",
            "preprocess": "/preprocess (POST)",
            "batch_preprocess": "/batch-preprocess (POST)"
        },
        "available_operations": [
            "clean",
            "normalize",
            "remove_urls",
            "remove_emails"
        ]
    }), 200


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Preprocessing Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
