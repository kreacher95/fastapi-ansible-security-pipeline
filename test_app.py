from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running smoothly"

def test_generate_hash():
    response = client.post("/hash", json={"text": "hello world"})
    assert response.status_code == 200
    # Expected SHA-256 for 'hello world'
    assert response.json()["hash"] == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"

def test_mask_pii():
    sample_text = "SSN is 123-45-6789 and card is 1234-5678-9012-3456"
    response = client.post("/mask-pii", json={"text": sample_text})
    assert response.status_code == 200
    assert "***-**-****" in response.json()["masked_text"]
    assert "****-****-****-****" in response.json()["masked_text"]

def test_validate_password_weak():
    response = client.post("/validate-password", json={"password": "short"})
    assert response.status_code == 200
    assert response.json()["is_strong"] is False

def test_validate_password_strong():
    response = client.post("/validate-password", json={"password": "P@ssword123!"})
    assert response.status_code == 200
    assert response.json()["is_strong"] is True