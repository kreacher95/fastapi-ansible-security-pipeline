import re
import hashlib
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Security Utility API")


# Request/Response Models
class HashRequest(BaseModel):
    text: str = Field(..., description="Text to generate SHA-256 hash for")

class MaskPiiRequest(BaseModel):
    text: str = Field(..., description="Text containing potential PII to mask")

class PasswordCheckRequest(BaseModel):
    password: str = Field(..., description="Password string to validate")


@app.get("/")
def health_check():
    return {"service": "Security Utility API", "status": "running smoothly"}


@app.post("/hash")
def generate_hash(payload: HashRequest):
    """Generate SHA-256 cryptographic hash of input text."""
    hashed_value = hashlib.sha256(payload.text.encode("utf-8")).hexdigest()
    return {
        "original_length": len(payload.text),
        "algorithm": "sha256",
        "hash": hashed_value
    }


@app.post("/mask-pii")
def mask_pii(payload: MaskPiiRequest):
    """Mask Social Security Numbers and 16-digit Card Numbers in input text."""
    masked_text = payload.text
    
    # Redact SSN patterns (XXX-XX-XXXX)
    masked_text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "***-**-****", masked_text)
    
    # Redact 16-digit card numbers (XXXX-XXXX-XXXX-XXXX or XXXXXXXXXXXXXXXX)
    masked_text = re.sub(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", "****-****-****-****", masked_text)
    
    return {
        "original_text": payload.text,
        "masked_text": masked_text
    }


@app.post("/validate-password")
def validate_password(payload: PasswordCheckRequest):
    """Evaluate password strength and complexity requirements."""
    pwd = payload.password
    checks = {
        "min_length_8": len(pwd) >= 8,
        "has_uppercase": bool(re.search(r"[A-Z]", pwd)),
        "has_lowercase": bool(re.search(r"[a-z]", pwd)),
        "has_digit": bool(re.search(r"\d", pwd)),
        "has_special_char": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd))
    }
    
    score = sum(checks.values())
    is_strong = score == 5
    
    return {
        "is_strong": is_strong,
        "score": f"{score}/5",
        "details": checks
    }