"""
Structura AI - Data Contracts & Pydantic Schemas
Defines strict JSON contracts for multimodal AI analysis, PPE audit,
structural diagnostics, and project valuation.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class PPEItemStatus(BaseModel):
    item: str = Field(..., description="Name of the PPE item (e.g. Safety Helmet, High-Vis Vest)")
    detected: bool = Field(..., description="Whether the PPE item is properly worn")
    status: str = Field(..., description="Compliant, Missing, or Non-Standard")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence score")
    notes: Optional[str] = Field(None, description="Observation details")


class SiteHazard(BaseModel):
    hazard_id: str
    hazard_type: str = Field(..., description="Category: Fall Risk, Electrical, Tripping, Scaffolding, PPE Violation")
    severity: str = Field(..., description="Low, Medium, High, or Critical")
    description: str = Field(..., description="Specific observation on site")
    standard_violated: str = Field(..., description="OSHA 1926 or IS 456 / IS 3696 citation")
    corrective_remedy: str = Field(..., description="Immediate engineering or administrative action required")


class PPEAuditResult(BaseModel):
    safety_score: int = Field(..., ge=0, le=100, description="Overall compliance safety score (0-100)")
    overall_status: str = Field(..., description="Compliant, Needs Attention, or Hazardous")
    workers_detected: int = Field(..., ge=0, description="Estimated number of workers detected")
    ppe_checklist: List[PPEItemStatus] = Field(default_factory=list)
    hazards_identified: List[SiteHazard] = Field(default_factory=list)
    inspection_timestamp: str
    regulatory_framework: str = "OSHA 1926 & IS 456:2000"


class CrackDiagnosisResult(BaseModel):
    defect_type: str = Field(..., description="Hairline, Settlement, Structural Shear, Thermal Expansion, Spalling")
    severity: str = Field(..., description="Low, Medium, High, or Critical")
    estimated_width_mm: float = Field(..., description="Estimated crack aperture in millimeters")
    structural_risk_level: str = Field(..., description="Cosmetic, Non-Structural, Progressive Structural, Critical Failure Hazard")
    probable_root_causes: List[str] = Field(default_factory=list)
    recommended_engineering_repairs: List[str] = Field(default_factory=list)
    repair_methodology: str = Field(..., description="e.g. Epoxy Pressure Injection, Polymer Modified Mortar, Carbon Fiber Stitching")
    monitoring_urgency: str = Field(..., description="Immediate Evacuation / Immediate Repair / Repair within 14 Days / Periodic Monitoring")
    is456_compliance_notes: str


class CostValuationEstimate(BaseModel):
    structure_type: str
    built_up_sqft: float
    location_tier: str
    city_tier_multiplier: float
    completion_percentage: float
    base_rate_per_sqft_inr: float
    total_project_budget_inr: float
    capex_incurred_inr: float
    current_asset_valuation_inr: float
    projected_completed_valuation_inr: float
    steel_required_tonnes: float
    cement_required_bags: float
    sand_required_cft: float
    aggregates_required_cft: float
    timeline_milestone: str


class WeatherSafetyAdvisory(BaseModel):
    condition: str
    ambient_temp_c: float
    wind_speed_kmh: float
    precipitation_prob: float
    risk_level: str
    crane_operations: str
    hot_work_protocol: str
    electrical_safety: str
    concrete_curing_advisory: str
    worker_shift_adjustments: str
