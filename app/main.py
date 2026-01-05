"""FastAPI application entry point."""
import json
import logging
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.settings import settings
from app.schemas import LeadRequest, LeadResponse, HealthResponse
from app.utils import normalize_lead, validate_lead, generate_dedupe_key
from app.ai import analyze_lead


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Lead Intake & CRM Automation",
    description="API for processing leads with AI classification and analysis",
    version="1.0.0"
)

# Add CORS middleware for Make.com webhooks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to Make.com IPs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@app.post("/lead", response_model=LeadResponse)
async def process_lead(lead: LeadRequest, request: Request):
    """
    Process incoming lead: validate, normalize, analyze with AI, and return structured response.
    
    This endpoint is designed to be called by Make.com webhooks.
    """
    try:
        # Normalize the lead data
        normalized_lead = normalize_lead(lead)
        
        # Validate the lead
        is_valid, error_message = validate_lead(normalized_lead)
        if not is_valid:
            logger.warning(f"Lead validation failed: {error_message}")
            raise HTTPException(status_code=400, detail=error_message)
        
        # Generate dedupe key
        dedupe_key = generate_dedupe_key(normalized_lead)
        
        # Analyze with AI
        logger.info(f"Analyzing lead with dedupe_key: {dedupe_key}")
        ai_analysis = await analyze_lead(
            name=normalized_lead.name,
            email=normalized_lead.email,
            company=normalized_lead.company,
            message=normalized_lead.message,
            source=normalized_lead.source
        )
        
        # Prepare raw payload JSON (stringified original request)
        raw_payload = lead.model_dump(exclude_none=True)
        raw_payload_json = json.dumps(raw_payload)
        
        # Build response
        response = LeadResponse(
            timestamp=datetime.utcnow().isoformat() + "Z",
            name=normalized_lead.name,
            email=normalized_lead.email,
            company=normalized_lead.company,
            message=normalized_lead.message,
            source=normalized_lead.source,
            dedupe_key=dedupe_key,
            intent=ai_analysis["intent"],
            urgency=ai_analysis["urgency"],
            budget_range=ai_analysis.get("budget_range"),
            summary=ai_analysis["summary"],
            lead_score=ai_analysis["lead_score"],
            next_action=ai_analysis["next_action"],
            raw_payload_json=raw_payload_json
        )
        
        logger.info(f"Successfully processed lead: {dedupe_key}, score: {ai_analysis['lead_score']}, urgency: {ai_analysis['urgency']}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing lead: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )

