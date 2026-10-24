"""
Structura AI - Multimodal AI Engine
Integrates Google Gemini 1.5/2.0 multimodal models with strict JSON contracts,
and includes an intelligent enterprise demonstration fallback mode when no API key
is supplied or if network quotas are exceeded.
"""

import os
import json
import io
import datetime
from typing import Dict, Any, Tuple, Optional
from PIL import Image

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


PPE_AUDIT_PROMPT = """
You are Structura AI's Senior Construction Safety Inspector operating under OSHA 1926 standards and Indian Standard IS 456 / IS 3696.
Analyze the provided construction site photo for worker PPE compliance and occupational hazards.

Return ONLY a valid, parseable JSON object matching this schema (no markdown fences, no explanatory text):
{
  "safety_score": <integer from 0 to 100>,
  "overall_status": "<Compliant | Needs Attention | Hazardous>",
  "workers_detected": <integer count>,
  "ppe_checklist": [
    {
      "item": "Hard Hat / Safety Helmet (IS 2925)",
      "detected": true/false,
      "status": "Compliant | Missing | Non-Standard",
      "confidence": <float 0.0 to 1.0>,
      "notes": "<observation>"
    },
    {
      "item": "High-Visibility Reflective Vest",
      "detected": true/false,
      "status": "Compliant | Missing | Non-Standard",
      "confidence": <float 0.0 to 1.0>,
      "notes": "<observation>"
    },
    {
      "item": "Steel-Toe Protective Footwear (IS 15298)",
      "detected": true/false,
      "status": "Compliant | Missing | Non-Standard",
      "confidence": <float 0.0 to 1.0>,
      "notes": "<observation>"
    },
    {
      "item": "Fall Arrest Harness & Lanyard (OSHA 1926.502)",
      "detected": true/false,
      "status": "Compliant | Missing | Non-Standard",
      "confidence": <float 0.0 to 1.0>,
      "notes": "<observation>"
    },
    {
      "item": "Eye / Face Shield Protection",
      "detected": true/false,
      "status": "Compliant | Missing | Non-Standard",
      "confidence": <float 0.0 to 1.0>,
      "notes": "<observation>"
    }
  ],
  "hazards_identified": [
    {
      "hazard_id": "HAZ-001",
      "hazard_type": "<Fall Risk | Electrical | Tripping | Scaffolding | PPE Violation>",
      "severity": "<Low | Medium | High | Critical>",
      "description": "<detailed observation>",
      "standard_violated": "<OSHA 1926.xxx or IS 456 section>",
      "corrective_remedy": "<actionable corrective action>"
    }
  ],
  "inspection_timestamp": "<ISO timestamp>",
  "regulatory_framework": "OSHA 1926 & IS 456:2000"
}
"""

CRACK_DIAGNOSIS_PROMPT = """
You are Structura AI's Senior Structural Forensic Engineer operating under IS 456:2000 and ACI 224R-01 (Control of Cracking in Concrete Structures).
Analyze the concrete/masonry wall image to diagnose crack morphology and evaluate structural risk.

Return ONLY a valid, parseable JSON object matching this schema (no markdown fences, no explanatory text):
{
  "defect_type": "<Hairline | Settlement | Structural Shear | Thermal Expansion | Spalling>",
  "severity": "<Low | Medium | High | Critical>",
  "estimated_width_mm": <float estimated crack width in mm, e.g. 0.8>,
  "structural_risk_level": "<Cosmetic | Non-Structural | Progressive Structural | Critical Failure Hazard>",
  "probable_root_causes": [
    "<cause 1>",
    "<cause 2>"
  ],
  "recommended_engineering_repairs": [
    "<repair step 1>",
    "<repair step 2>"
  ],
  "repair_methodology": "<e.g. Low-viscosity epoxy pressure injection (ASTM C881) followed by carbon-fiber fabric wrapping>",
  "monitoring_urgency": "<Immediate Evacuation | Immediate Repair | Repair within 14 Days | Periodic Monitoring>",
  "is456_compliance_notes": "<summary of compliance regarding permissible crack width under IS 456 clause 35.3.2>"
}
"""


def _clean_json_response(raw_text: str) -> Dict[str, Any]:
    """Strips markdown code blocks and parses raw text into a Python dict."""
    cleaned = raw_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    return json.loads(cleaned)


def analyze_ppe_safety(
    image: Image.Image,
    api_key: Optional[str] = None
) -> Tuple[Dict[str, Any], bool]:
    """
    Analyzes construction site photo for PPE compliance.
    Returns (result_dict, is_demo_mode).
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if api_key and api_key.strip() and GENAI_AVAILABLE:
        try:
            client = genai.Client(api_key=api_key.strip())
            # Convert PIL image to bytes
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_bytes = buffered.getvalue()

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                    PPE_AUDIT_PROMPT
                ],
            )
            data = _clean_json_response(response.text)
            data["inspection_timestamp"] = timestamp
            return data, False
        except Exception:
            # Fall back gracefully to demo analysis
            pass

    # High-fidelity realistic demonstration fallback
    demo_result = {
        "safety_score": 78,
        "overall_status": "Needs Attention",
        "workers_detected": 4,
        "ppe_checklist": [
            {
                "item": "Hard Hat / Safety Helmet (IS 2925)",
                "detected": True,
                "status": "Compliant",
                "confidence": 0.94,
                "notes": "3 of 4 workers observed wearing Class E industrial safety helmets."
            },
            {
                "item": "High-Visibility Reflective Vest",
                "detected": True,
                "status": "Compliant",
                "confidence": 0.91,
                "notes": "Fluorescent high-vis orange/yellow vests visible with retroreflective bands."
            },
            {
                "item": "Steel-Toe Protective Footwear (IS 15298)",
                "detected": True,
                "status": "Compliant",
                "confidence": 0.86,
                "notes": "Ankle-high protective footwear present in active work staging zone."
            },
            {
                "item": "Fall Arrest Harness & Lanyard (OSHA 1926.502)",
                "detected": False,
                "status": "Missing",
                "confidence": 0.96,
                "notes": "Worker active on elevated scaffold (>2.4m) without tethered safety harness."
            },
            {
                "item": "Eye / Face Shield Protection",
                "detected": False,
                "status": "Missing",
                "confidence": 0.88,
                "notes": "Worker in proximity of cutting equipment lacks impact-resistant safety goggles."
            }
        ],
        "hazards_identified": [
            {
                "hazard_id": "HAZ-001",
                "hazard_type": "Fall Risk",
                "severity": "Critical",
                "description": "Scaffold working platform exceeds 2.0 meters without secondary toe-boards or anchored personal fall arrest harness.",
                "standard_violated": "OSHA 1926.451(g) / IS 3696: Part 1",
                "corrective_remedy": "Cease elevated work immediately. Install perimeter guardrail system and secure 100% tie-off lifelines."
            },
            {
                "hazard_id": "HAZ-002",
                "hazard_type": "Tripping / Housekeeping",
                "severity": "Medium",
                "description": "Trailing unbundled 3-phase electrical cables and loose rebar offcuts crossing main pedestrian access path.",
                "standard_violated": "OSHA 1926.25(a) / IS 4014",
                "corrective_remedy": "Clear pedestrian access aisle. Elevate temporary power conduits to minimum 2.1m clearance using insulated hooks."
            },
            {
                "hazard_id": "HAZ-003",
                "hazard_type": "PPE Violation",
                "severity": "High",
                "description": "One laborer observed in active crane swing-radius without industrial protective headgear.",
                "standard_violated": "OSHA 1926.100 / IS 2925",
                "corrective_remedy": "Issue immediate stop-work warning, escort laborer from zone, and equip with certified ANSI Z89.1 / IS 2925 helmet."
            }
        ],
        "inspection_timestamp": timestamp,
        "regulatory_framework": "OSHA 1926 & IS 456:2000"
    }
    return demo_result, True


def analyze_crack_diagnostics(
    image: Image.Image,
    api_key: Optional[str] = None
) -> Tuple[Dict[str, Any], bool]:
    """
    Analyzes concrete surface for crack classification and structural integrity.
    Returns (result_dict, is_demo_mode).
    """
    if api_key and api_key.strip() and GENAI_AVAILABLE:
        try:
            client = genai.Client(api_key=api_key.strip())
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_bytes = buffered.getvalue()

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                    CRACK_DIAGNOSIS_PROMPT
                ],
            )
            data = _clean_json_response(response.text)
            return data, False
        except Exception:
            pass

    # High-fidelity realistic demonstration fallback
    demo_result = {
        "defect_type": "Structural Shear Crack",
        "severity": "High",
        "estimated_width_mm": 2.4,
        "structural_risk_level": "Progressive Structural Risk",
        "probable_root_causes": [
            "Excessive diagonal tension shear stress exceeding member shear capacity (Tau_c max per IS 456 Table 20).",
            "Differential foundation settlement causing secondary rotational stresses at beam-column junction.",
            "Sub-optimal stirrups spacing and missing closed shear links in the critical plastic hinge zone."
        ],
        "recommended_engineering_repairs": [
            "Install mechanical crack monitors (Avongard gauges) to measure 14-day progressive dynamic displacement.",
            "Drill staggered injection ports along crack path at 150mm intervals.",
            "Execute low-viscosity structural epoxy resin pressure injection conforming to ASTM C881 Type IV.",
            "Apply two layers of unidirectional Carbon Fiber Reinforced Polymer (CFRP) fabric laminate wrap around beam web for shear capacity enhancement."
        ],
        "repair_methodology": "High-Pressure Epoxy Resins Injection (ASTM C881) combined with externally bonded Carbon Fiber Fabric (CFRP) confining wrap.",
        "monitoring_urgency": "Immediate Repair (Within 7 Days)",
        "is456_compliance_notes": "Permissible crack width under IS 456 Clause 35.3.2 is 0.3mm for moderate exposure. Observed 2.4mm exceeds safety limits by 800%."
    }
    return demo_result, True


def get_assistant_chat_response(
    messages: list,
    api_key: Optional[str] = None,
    current_weather: Optional[str] = None
) -> str:
    """
    Generates intelligent construction engineering multi-turn assistant responses.
    """
    system_instruction = (
        "You are Structura AI's Senior Construction Engineering and Project Intelligence Consultant. "
        "You provide expert civil engineering advice, OSHA safety protocols, Indian Standard codes (IS 456, IS 800, IS 1893, IS 1926), "
        "cost estimation, concrete mix designs, and equipment management. "
        "Be professional, precise, actionable, and cite relevant engineering standards where applicable."
    )
    if current_weather:
        system_instruction += f"\nCurrent active site weather alert: {current_weather}."

    if api_key and api_key.strip() and GENAI_AVAILABLE:
        try:
            client = genai.Client(api_key=api_key.strip())
            # Format chat history
            contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(f"{role.capitalize()}: {msg['content']}")
            prompt = system_instruction + "\n\nConversation:\n" + "\n".join(contents) + "\nModel:"
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception:
            pass

    # Intelligent contextual fallback responses
    last_user_msg = messages[-1]["content"].lower() if messages else ""

    if "safety" in last_user_msg or "osha" in last_user_msg or "ppe" in last_user_msg:
        return (
            "**Safety Protocol Advisory (OSHA 1926 & IS 3696):**\n\n"
            "1. **Fall Protection (OSHA 1926.501):** Any working surface with an unprotected side or edge that is 6 feet (1.8m) or higher must be protected via guardrail systems, safety net systems, or personal fall arrest systems (PFAS).\n"
            "2. **Scaffolding Inspection:** Verify daily Green Safety Scaff-Tags issued by the designated Competent Person before morning shift kickoff.\n"
            "3. **Head Protection (IS 2925):** Full-time Class E impact-tested helmets are mandatory within active crane radius and formwork strike zones."
        )
    elif "crack" in last_user_msg or "concrete" in last_user_msg or "curing" in last_user_msg:
        return (
            "**Concrete & Structural Engineering Advisory (IS 456:2000):**\n\n"
            "1. **Permissible Crack Limits:** IS 456 Clause 35.3.2 specifies maximum allowable crack widths of 0.3mm for moderate exposure and 0.2mm for severe/coastal exposure.\n"
            "2. **Curing Cycle:** Minimum moist curing duration is 7 days for Ordinary Portland Cement (OPC) and 10 days for mineral-admixture concrete (Fly ash/GGBS).\n"
            "3. **Structural Shear Mitigation:** For diagonal tension cracks, assess shear reinforcement ratio (Av/b*s) against Tau_v > Tau_c and consider low-viscosity epoxy pressure grouting (ASTM C881)."
        )
    elif "cost" in last_user_msg or "budget" in last_user_msg or "rate" in last_user_msg:
        return (
            "**Cost & Estimation Advisory (CPWD Plinth Area Rates):**\n\n"
            "1. **Tier 1 Metro RCC Framing:** Averages ₹2,100 - ₹2,800/sqft for standard residential superstructure.\n"
            "2. **Material Consumption Ratios:** Standard thumb rules dictate ~3.8-4.5 kg of TMT FE500D steel per sqft and ~0.4-0.45 bags of 53-grade OPC cement per sqft of built-up area.\n"
            "3. **Contingency Reserve:** Always allocate 5-8% unallocated CapEx reserve for volatile cement/steel commodity index fluctuations."
        )
    elif "weather" in last_user_msg or "crane" in last_user_msg or "wind" in last_user_msg:
        return (
            "**Adverse Weather Site Advisory:**\n\n"
            "1. **High Wind Threshold:** Under OSHA 1926.1431 and standard manufacturer charts, tower crane lifting operations must be suspended when sustained wind speeds exceed 38 mph (61 km/h or Beaufort Force 7).\n"
            "2. **Precipitation Safeguards:** Cover green concrete pours with waterproof tarpaulins to avoid altering the water-cement ratio, which drastically compromises 28-day characteristic compressive strength (fck)."
        )
    else:
        return (
            "**Structura AI Site Engineering Desk:**\n\n"
            "I am ready to assist with:\n"
            "- Structural defect diagnostics and crack classification under IS 456:2000.\n"
            "- Multi-point PPE compliance audits & OSHA 1926 hazard mitigation.\n"
            "- Material quantification (TMT steel, 53-grade cement, M-sand) & valuation.\n"
            "- Weather-contingent site operation checklists.\n\n"
            "How can I assist your ongoing site operations today?"
        )
