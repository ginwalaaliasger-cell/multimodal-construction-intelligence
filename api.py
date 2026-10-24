"""
Structura AI - FastAPI REST Microservice
Provides REST endpoints and strict JSON data contracts for:
- PPE Safety Audit & Hazard Classification
- Concrete Crack Diagnostics & Structural Risk Analysis
- Project Cost Estimation, Material Quantities & Real Estate Valuation
- Weather-Aware Construction Protocols
- Engineering Advisory Chatbot
"""

import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import io

from services.contracts import (
    PPEAuditResult,
    CrackDiagnosisResult,
    CostValuationEstimate,
    WeatherSafetyAdvisory
)
from services.ai_engine import (
    analyze_ppe_safety,
    analyze_crack_diagnostics,
    get_assistant_chat_response
)
from services.cost_estimator import calculate_project_valuation
from services.weather_advisory import get_weather_advisory, WEATHER_PRESETS
from services.architectural_visualizer import generate_architectural_render_url

app = FastAPI(
    title="Structura AI - Multimodal Construction Intelligence API",
    description="Enterprise Decision-Support REST API for Construction Safety, Structural Integrity, Valuation & Site Operations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ValuationRequest(BaseModel):
    structure_type: str = "Residential (RCC Frame - Standard)"
    built_up_sqft: float = 12500.0
    location_tier: str = "Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Chennai)"
    completion_percentage: float = 45.0


class ChatRequest(BaseModel):
    message: str
    weather_condition: Optional[str] = "Normal / Favorable Weather"
    api_key: Optional[str] = None


@app.get("/")
def health_check():
    return {
        "status": "online",
        "platform": "Structura AI - Multimodal Construction Intelligence",
        "version": "1.0.0",
        "endpoints": [
            "/api/v1/safety/audit-ppe",
            "/api/v1/structural/diagnose-crack",
            "/api/v1/planning/estimate-valuation",
            "/api/v1/site/weather-advisory",
            "/api/v1/assistant/chat",
            "/docs"
        ]
    }


@app.post("/api/v1/safety/audit-ppe", response_model=PPEAuditResult)
async def audit_site_safety(
    file: UploadFile = File(...),
    api_key: Optional[str] = Form(None)
):
    """Audits uploaded construction site image for PPE compliance under OSHA 1926 & IS 456."""
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        result_dict, is_demo = analyze_ppe_safety(image, api_key=api_key)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")


@app.post("/api/v1/structural/diagnose-crack", response_model=CrackDiagnosisResult)
async def diagnose_structural_crack(
    file: UploadFile = File(...),
    api_key: Optional[str] = Form(None)
):
    """Diagnoses concrete crack defect type, severity, and repair methodology under IS 456."""
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        result_dict, is_demo = analyze_crack_diagnostics(image, api_key=api_key)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crack diagnosis failed: {str(e)}")


@app.post("/api/v1/planning/estimate-valuation", response_model=CostValuationEstimate)
def estimate_cost_and_valuation(req: ValuationRequest):
    """Calculates project budget, CapEx, asset valuation (INR), and material metrics."""
    return calculate_project_valuation(
        structure_type=req.structure_type,
        built_up_sqft=req.built_up_sqft,
        location_tier=req.location_tier,
        completion_percentage=req.completion_percentage
    )


@app.get("/api/v1/site/weather-advisory", response_model=WeatherSafetyAdvisory)
def fetch_weather_advisory(condition: str = Query("Normal / Favorable Weather")):
    """Returns dynamic site safety protocol alerts based on weather condition."""
    return get_weather_advisory(condition)


@app.post("/api/v1/assistant/chat")
def site_assistant_chat(req: ChatRequest):
    """Interacts with the multi-turn construction engineering assistant."""
    messages = [{"role": "user", "content": req.message}]
    response_text = get_assistant_chat_response(
        messages=messages,
        api_key=req.api_key,
        current_weather=req.weather_condition
    )
    return {"response": response_text}


@app.get("/api/v1/planning/concept-render")
def get_concept_render(
    structure_type: str = "Commercial Office Complex",
    built_up_sqft: float = 25000.0,
    style: str = "Modern Sustainable Biophilic"
):
    """Generates 3D concept architectural rendering URL via Pollinations AI."""
    url = generate_architectural_render_url(
        structure_type=structure_type,
        built_up_sqft=built_up_sqft,
        architectural_style=style
    )
    return {"render_url": url}
