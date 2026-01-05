"""Utility functions for validation, normalization, and deduplication."""
import hashlib
import json
import re
from typing import Optional
from app.schemas import LeadRequest


def normalize_email(email: Optional[str]) -> Optional[str]:
    """
    Normalize email: lowercase and trim whitespace.
    
    Args:
        email: Raw email string
        
    Returns:
        Normalized email or None if invalid/empty
    """
    if not email:
        return None
    
    email = email.strip().lower()
    
    # Basic email validation regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return None
    
    return email


def normalize_string(value: Optional[str], max_length: Optional[int] = None) -> Optional[str]:
    """
    Normalize string: trim whitespace and optionally limit length.
    
    Args:
        value: Raw string value
        max_length: Optional maximum length
        
    Returns:
        Normalized string or None if empty
    """
    if not value:
        return None
    
    normalized = value.strip()
    
    if max_length and len(normalized) > max_length:
        normalized = normalized[:max_length]
    
    return normalized if normalized else None


def validate_lead(lead: LeadRequest) -> tuple[bool, Optional[str]]:
    """
    Validate lead data according to business rules.
    
    Args:
        lead: LeadRequest object
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Message is required (already validated in schema, but double-check)
    if not lead.message or not lead.message.strip():
        return False, "message is required and cannot be empty"
    
    # At least one contact method required
    if not lead.has_contact_info():
        return False, "at least one of 'email' or 'name' must be provided"
    
    # Message length check (schema handles max, but validate here too)
    if len(lead.message) > 4000:
        return False, "message exceeds maximum length of 4000 characters"
    
    return True, None


def generate_dedupe_key(lead: LeadRequest) -> str:
    """
    Generate a stable deduplication key for the lead.
    
    Strategy:
    - If email is present: use normalized email
    - Else: hash of (normalized name + normalized company)
    
    Args:
        lead: LeadRequest object
        
    Returns:
        Deduplication key string
    """
    # Normalize email if present
    normalized_email = normalize_email(lead.email)
    
    if normalized_email:
        return normalized_email
    
    # Fallback to hash of name + company
    name_part = normalize_string(lead.name) or ""
    company_part = normalize_string(lead.company) or ""
    
    combined = f"{name_part}|{company_part}"
    
    # Generate stable hash
    hash_obj = hashlib.sha256(combined.encode('utf-8'))
    return f"hash_{hash_obj.hexdigest()[:16]}"


def normalize_lead(lead: LeadRequest) -> LeadRequest:
    """
    Normalize all fields in a lead request.
    
    Args:
        lead: LeadRequest object
        
    Returns:
        New LeadRequest with normalized fields
    """
    return LeadRequest(
        name=normalize_string(lead.name),
        email=normalize_email(lead.email),
        company=normalize_string(lead.company),
        message=normalize_string(lead.message) or lead.message,  # Message required, so keep original if normalization fails
        source=normalize_string(lead.source)
    )

