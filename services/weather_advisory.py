"""
Structura AI - Weather-Aware Site Advisory Engine
Provides OSHA & IS 456-compliant construction safety protocols based on
meteorological conditions and micro-climate hazards.
"""

from typing import Dict, Any
from .contracts import WeatherSafetyAdvisory

WEATHER_PRESETS: Dict[str, Dict[str, Any]] = {
    "Normal / Favorable Weather": {
        "condition": "Normal / Favorable Weather",
        "temp": 28.5,
        "wind": 14.0,
        "precip": 5.0,
        "risk_level": "Low",
        "crane_operations": "Full clearance active. Maintain standard anemometer monitoring above 30m hoist height.",
        "hot_work": "Standard hot work permits apply. Fire watch active for 30 minutes post-welding.",
        "electrical": "Standard dry-condition checks. Routine RCD/GFCI verification on distribution boxes.",
        "concrete_curing": "Standard wet burlap or ponding method. Minimum 7 to 10 days curing cycle under IS 456.",
        "worker_shifts": "Standard 8-hour shift schedule with routine 15-minute hydration intervals."
    },
    "High Wind / Gale Warning": {
        "condition": "High Wind / Gale Warning",
        "temp": 24.0,
        "wind": 58.0,
        "precip": 20.0,
        "risk_level": "Critical",
        "crane_operations": "MANDATORY SHUTDOWN: Suspend all tower crane lifts, suspended gondolas, and mobile hoist operations immediately. Engage jib windmilling / slew brake release per manufacturer protocol.",
        "hot_work": "Restrict all exterior elevated cutting and grinding to prevent airborne incandescent slag dispersion.",
        "electrical": "Inspect elevated temporary wiring, secure overhead service masts, de-energize loose perimeter festoon cables.",
        "concrete_curing": "High surface evaporation rate: Apply liquid curing membranes immediately post-finish to prevent plastic shrinkage cracking.",
        "worker_shifts": "Evacuate personnel from scaffolding tiers above Level 4. Restrict all roof-deck edge decking activities."
    },
    "Heavy Monsoon Rain / Waterlogging": {
        "condition": "Heavy Monsoon Rain / Waterlogging",
        "temp": 22.5,
        "wind": 32.0,
        "precip": 92.0,
        "risk_level": "High",
        "crane_operations": "Ground bearing capacity compromised: Check outrigger pad sub-base for soil liquefaction before any mobile crane setup.",
        "hot_work": "Strict ban on all outdoor arc welding and electrical cutting due to extreme electrocution hazards.",
        "electrical": "MANDATORY TRIP AUDIT: Power down all non-essential temporary supply panels. Verify IP65 water ingress seals on all site distribution boxes.",
        "concrete_curing": "HALT POURING: Cease all structural concrete placement. Unset concrete must be covered with heavy tarpaulins to prevent water-cement ratio alteration.",
        "worker_shifts": "High slipping hazard. Suspend all steep-pitch roofing and trench excavations due to mudslide / cave-in risks."
    },
    "Extreme Heat Wave (> 42°C)": {
        "condition": "Extreme Heat Wave (> 42°C)",
        "temp": 43.5,
        "wind": 9.0,
        "precip": 0.0,
        "risk_level": "High",
        "crane_operations": "Hydraulic oil temperature surveillance: Monitor fluid viscosity and cabin HVAC health to avoid crane operator fatigue.",
        "hot_work": "Heightened flash ignition danger: Store fuel gas cylinders under shaded, ventilated barriers away from direct solar radiation.",
        "electrical": "Transformer and motor thermal monitoring: Ensure air vents on generator sets are unobstructed to prevent thermal overload shutdowns.",
        "concrete_curing": "RAPID DESICCATION ALERT: Add set-retarders to concrete mix. Pre-cool aggregate batches with chilled water. Double ponding frequency to avoid structural thermal shock.",
        "worker_shifts": "IMPLEMENT OS-HEAT PROTOCOL: Mandatory split shifts (6:00 AM - 11:30 AM & 3:30 PM - 7:00 PM). Supply electrolyte ORS stations every 50 meters."
    }
}


def get_weather_advisory(condition_key: str) -> WeatherSafetyAdvisory:
    """Returns dynamic safety advisory based on selected weather condition."""
    data = WEATHER_PRESETS.get(condition_key, WEATHER_PRESETS["Normal / Favorable Weather"])
    return WeatherSafetyAdvisory(
        condition=data["condition"],
        ambient_temp_c=data["temp"],
        wind_speed_kmh=data["wind"],
        precipitation_prob=data["precip"],
        risk_level=data["risk_level"],
        crane_operations=data["crane_operations"],
        hot_work_protocol=data["hot_work"],
        electrical_safety=data["electrical"],
        concrete_curing_advisory=data["concrete_curing"],
        worker_shift_adjustments=data["worker_shifts"]
    )
