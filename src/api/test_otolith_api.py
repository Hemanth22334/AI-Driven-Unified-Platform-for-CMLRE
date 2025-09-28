import json
import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_analyze_otolith_success(client):
    """Test the /api/otolith/analyze endpoint with valid data."""
    payload = {
        "shape_coordinates": [1, 2, 3],
        "area": 100,
        "perimeter": 40
    }
    response = client.post('/api/otolith/analyze',
                             data=json.dumps(payload),
                             content_type='application/json')

    assert response.status_code == 200
    data = response.get_json()
    assert "classification" in data
    assert "visualization_url" in data

def test_analyze_otolith_missing_fields(client):
    """Test the endpoint with missing fields in the payload."""
    payload = {
        "shape_coordinates": [1, 2, 3],
        "area": 100
    }
    response = client.post('/api/otolith/analyze',
                             data=json.dumps(payload),
                             content_type='application/json')

    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == "Missing required fields"

def test_analyze_otolith_invalid_input(client):
    """Test the endpoint with non-JSON data."""
    response = client.post('/api/otolith/analyze',
                             data="not json",
                             content_type='text/plain')

    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == "Invalid input, expected JSON"