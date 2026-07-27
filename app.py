import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes

app = FastAPI(title="Crypto & Security Service API")

# Generate a temporary encryption key for the app session
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

class Payload(BaseModel):
    data: str

@app.get("/")
def health_check():
    """Health check endpoint for deployment validation."""
    return {"status": "running smoothly", "service": "Security API"}

@app.post("/encrypt")
def encrypt_message(payload: Payload):
    """Encrypts input text using AES (Fernet implementation)."""
    if not payload.data:
        raise HTTPException(status_code=400, detail="Data cannot be empty")
    
    encrypted_bytes = cipher.encrypt(payload.data.encode())
    return {
        "original": payload.data,
        "encrypted_token": encrypted_bytes.decode()
    }

@app.post("/hash")
def hash_payload(payload: Payload):
    """Generates a SHA-256 digest of input data."""
    digest = hashes.Hash(hashes.SHA256())
    digest.update(payload.data.encode())
    hash_result = digest.finalize()
    return {
        "original": payload.data,
        "sha256": base64.b64encode(hash_result).decode()
    }
