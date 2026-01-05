"""OpenAI integration for lead classification and analysis."""
import json
import logging
from typing import Dict, Any, Optional
import httpx
from app.settings import settings


logger = logging.getLogger(__name__)


# System and user prompts for OpenAI
SYSTEM_PROMPT = """You are an expert lead qualification assistant. Your task is to analyze incoming leads and return ONLY valid JSON with the following structure:

{
  "intent": "string describing the lead's primary intent (e.g., 'seeking AI automation', 'inquiry about services', 'partnership opportunity')",
  "urgency": "one of: low, medium, high",
  "budget_range": "string describing budget if mentioned (e.g., '5k-10k', '50k+', 'not specified') or null if not mentioned",
  "summary": "maximum 2 sentences summarizing the lead's needs and key information",
  "lead_score": integer between 0-100 representing lead quality (consider budget, urgency, company size, message clarity)",
  "next_action": "recommended next action for the sales team (e.g., 'schedule discovery call', 'send pricing info', 'qualify budget')"
}

CRITICAL RULES:
- Return ONLY valid JSON, no additional text, no markdown, no code blocks
- urgency MUST be exactly one of: "low", "medium", or "high"
- lead_score MUST be an integer between 0 and 100
- summary MUST be maximum 2 sentences
- budget_range can be a string or null (JSON null, not string "null")
- If budget is not mentioned, set budget_range to null
"""

USER_PROMPT_TEMPLATE = """Analyze this lead and return the JSON structure:

Name: {name}
Email: {email}
Company: {company}
Message: {message}
Source: {source}

Return ONLY valid JSON with keys: intent, urgency, budget_range, summary, lead_score, next_action"""


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from text, handling cases where model returns markdown or extra text.
    
    Args:
        text: Raw text response from OpenAI
        
    Returns:
        Parsed JSON dict or None if extraction fails
    """
    text = text.strip()
    
    # Try direct JSON parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from markdown code blocks
    if "```" in text:
        # Look for JSON code blocks
        import re
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
    
    # Try to find JSON object in text
    import re
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    
    return None


async def analyze_lead(
    name: Optional[str],
    email: Optional[str],
    company: Optional[str],
    message: str,
    source: Optional[str]
) -> Dict[str, Any]:
    """
    Call OpenAI to analyze and classify a lead.
    
    Args:
        name: Lead name
        email: Lead email
        company: Lead company
        message: Lead message
        source: Lead source
        
    Returns:
        Dictionary with: intent, urgency, budget_range, summary, lead_score, next_action
        
    Raises:
        Exception: If OpenAI call fails or returns invalid data
    """
    if settings.dry_run:
        logger.info("DRY_RUN mode: Returning mock AI analysis")
        return {
            "intent": "seeking AI automation services",
            "urgency": "medium",
            "budget_range": "5k-10k",
            "summary": "Lead is interested in AI lead system with budget of 5k. Requires ASAP implementation.",
            "lead_score": 75,
            "next_action": "schedule discovery call to discuss requirements"
        }
    
    # Build user prompt
    user_prompt = USER_PROMPT_TEMPLATE.format(
        name=name or "Not provided",
        email=email or "Not provided",
        company=company or "Not provided",
        message=message,
        source=source or "Not provided"
    )
    
    # Prepare OpenAI API request
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o-mini",  # Using cost-effective model
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,  # Lower temperature for more consistent JSON
        "response_format": {"type": "json_object"}  # Force JSON mode
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse JSON from response
            analysis = extract_json_from_text(content)
            
            if not analysis:
                # Retry with repair attempt
                logger.warning("Failed to parse JSON, attempting repair")
                repair_payload = payload.copy()
                repair_payload["messages"].append({
                    "role": "assistant",
                    "content": content
                })
                repair_payload["messages"].append({
                    "role": "user",
                    "content": "Return only valid JSON with no additional text."
                })
                
                retry_response = await client.post(url, headers=headers, json=repair_payload)
                retry_response.raise_for_status()
                retry_result = retry_response.json()
                retry_content = retry_result["choices"][0]["message"]["content"]
                analysis = extract_json_from_text(retry_content)
            
            if not analysis:
                raise ValueError("Failed to extract valid JSON from OpenAI response")
            
            # Validate required fields
            required_fields = ["intent", "urgency", "summary", "lead_score", "next_action"]
            missing_fields = [field for field in required_fields if field not in analysis]
            if missing_fields:
                raise ValueError(f"Missing required fields in AI response: {missing_fields}")
            
            # Validate urgency
            if analysis["urgency"] not in ["low", "medium", "high"]:
                logger.warning(f"Invalid urgency value: {analysis['urgency']}, defaulting to 'medium'")
                analysis["urgency"] = "medium"
            
            # Validate lead_score
            if not isinstance(analysis["lead_score"], int):
                try:
                    analysis["lead_score"] = int(analysis["lead_score"])
                except (ValueError, TypeError):
                    logger.warning(f"Invalid lead_score: {analysis['lead_score']}, defaulting to 50")
                    analysis["lead_score"] = 50
            
            # Clamp lead_score to 0-100
            analysis["lead_score"] = max(0, min(100, analysis["lead_score"]))
            
            # Ensure budget_range is None (not string "null") if not provided
            if "budget_range" not in analysis or analysis["budget_range"] == "null":
                analysis["budget_range"] = None
            
            return analysis
            
    except httpx.TimeoutException:
        logger.error("OpenAI API request timed out")
        raise Exception("AI analysis request timed out. Please try again.")
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenAI API error: {e.response.status_code} - {e.response.text}")
        raise Exception(f"AI analysis failed: {e.response.status_code}")
    except Exception as e:
        logger.error(f"Unexpected error in AI analysis: {str(e)}")
        raise Exception(f"AI analysis failed: {str(e)}")

