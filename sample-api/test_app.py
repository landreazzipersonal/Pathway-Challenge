"""
Basic test examples for the ML API
Candidates should expand these tests and add more comprehensive coverage.
"""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'version' in data


def test_readiness_check(client):
    """Test the readiness check endpoint"""
    response = client.get('/ready')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ready'


def test_metrics_endpoint(client):
    """Test the metrics endpoint"""
    response = client.get('/metrics')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_requests' in data
    assert 'model_version' in data


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'service' in data
    assert 'endpoints' in data


def test_predict_valid_input(client):
    """Test prediction with valid input"""
    response = client.post('/predict',
                          data=json.dumps({'text': 'This is a test sentence'}),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prediction' in data
    assert 'sentiment' in data['prediction']
    assert 'processing_time_seconds' in data


def test_predict_missing_text_field(client):
    """Test prediction with missing text field"""
    response = client.post('/predict',
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_predict_empty_text(client):
    """Test prediction with empty text"""
    response = client.post('/predict',
                          data=json.dumps({'text': ''}),
                          content_type='application/json')
    assert response.status_code == 400


def test_predict_invalid_content_type(client):
    """Test prediction with invalid content type"""
    response = client.post('/predict',
                          data='text=test',
                          content_type='application/x-www-form-urlencoded')
    assert response.status_code == 400


def test_batch_predict_valid_input(client):
    """Test batch prediction with valid input"""
    texts = ['First text', 'Second text', 'Third text']
    response = client.post('/batch-predict',
                          data=json.dumps({'texts': texts}),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'predictions' in data
    assert len(data['predictions']) == 3


def test_batch_predict_missing_texts_field(client):
    """Test batch prediction with missing texts field"""
    response = client.post('/batch-predict',
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400


def test_batch_predict_empty_array(client):
    """Test batch prediction with empty array"""
    response = client.post('/batch-predict',
                          data=json.dumps({'texts': []}),
                          content_type='application/json')
    assert response.status_code == 400


# TODO: Candidates should add more tests:
# - Test concurrent requests
# - Test rate limiting (if implemented)
# - Test error handling for various edge cases
# - Test integration with preprocessing service
# - Performance tests
# - Load tests
