from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    """Verify root endpoint returns 200 OK and expected status."""
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

def test_encrypt_endpoint_success():
    """Test successful encryption payload."""
    response = client.post("/encrypt", json={"data": "Secret Message"})
    assert response.status_code == 200
    data = response.json()
    assert data["original"] == "Secret Message"
    assert "encrypted_token" in data

def test_encrypt_endpoint_empty_data():
    """Test custom error handling when data is empty (400 Bad Request)."""
    response = client.post("/encrypt", json={"data": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Data cannot be empty"

def test_hash_endpoint_success():
    """Test SHA-256 hashing endpoint consistency."""
    payload = {"data": "Test string"}
    res1 = client.post("/hash", json=payload)
    res2 = client.post("/hash", json=payload)
    
    assert res1.status_code == 200
    # SHA-256 is deterministic: same input must equal same hash output
    assert res1.json()["sha256"] == res2.json()["sha256"]
