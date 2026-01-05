"""Pydantic models for request/response validation."""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field, field_validator


class LeadRequest(BaseModel):
    """Incoming lead data from Make.com webhook."""
    name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    message: str = Field(..., min_length=1, max_length=4000)
    source: Optional[str] = None
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Ensure message is not empty after stripping."""
        if not v or not v.strip():
            raise ValueError("message cannot be empty")
        return v.strip()
    
    def has_contact_info(self) -> bool:
        """Check if at least one contact field is present."""
        return bool(self.email or self.name)


class LeadResponse(BaseModel):
    """Structured lead response with AI analysis."""
    timestamp: str  # ISO8601 format
    name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    message: str
    source: Optional[str] = None
    dedupe_key: str
    intent: str
    urgency: Literal["low", "medium", "high"]
    budget_range: Optional[str] = None
    summary: str = Field(..., max_length=500)  # Max 2 sentences enforced in prompt
    lead_score: int = Field(..., ge=0, le=100)
    next_action: str
    raw_payload_json: str  # Stringified original request


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    timestamp: str

