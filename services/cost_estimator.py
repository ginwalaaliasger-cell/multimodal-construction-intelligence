"""
Structura AI - Construction Economics & Estimation Engine
Implements standard CPWD and IS-aligned material & valuation formulas
for Indian construction projects across Tier 1, 2, and 3 cities.
"""

from typing import Dict, Any
from .contracts import CostValuationEstimate

# Base rates per sqft for standard Indian construction (in INR)
STRUCTURE_RATES = {
    "Residential (RCC Frame - Standard)": {
        "base_rate": 2100.0,
        "steel_per_sqft_kg": 4.0,     # ~4 kg/sqft
        "cement_per_sqft_bags": 0.42, # ~0.42 bags/sqft
        "sand_per_sqft_cft": 1.8,     # ~1.8 cft/sqft
        "aggregate_per_sqft_cft": 1.35
    },
    "Residential (High-Rise Luxury)": {
        "base_rate": 3400.0,
        "steel_per_sqft_kg": 5.2,
        "cement_per_sqft_bags": 0.48,
        "sand_per_sqft_cft": 2.1,
        "aggregate_per_sqft_cft": 1.6
    },
    "Commercial Office Complex": {
        "base_rate": 3800.0,
        "steel_per_sqft_kg": 5.8,
        "cement_per_sqft_bags": 0.50,
        "sand_per_sqft_cft": 2.2,
        "aggregate_per_sqft_cft": 1.7
    },
    "Industrial Pre-Engineered Warehouse": {
        "base_rate": 1850.0,
        "steel_per_sqft_kg": 6.5,     # High structural steel
        "cement_per_sqft_bags": 0.30,
        "sand_per_sqft_cft": 1.4,
        "aggregate_per_sqft_cft": 1.1
    },
    "Institutional & Educational Campus": {
        "base_rate": 2600.0,
        "steel_per_sqft_kg": 4.5,
        "cement_per_sqft_bags": 0.44,
        "sand_per_sqft_cft": 1.9,
        "aggregate_per_sqft_cft": 1.45
    }
}

# City tier index multipliers (materials, logistics, and skilled labor cost factors)
CITY_TIERS = {
    "Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Chennai)": {
        "cost_multiplier": 1.25,
        "market_land_appreciation_multiplier": 1.65,
        "tier_name": "Tier 1 Metro"
    },
    "Tier 2 (Pune, Hyderabad, Ahmedabad, Kolkata, Kochi)": {
        "cost_multiplier": 1.10,
        "market_land_appreciation_multiplier": 1.35,
        "tier_name": "Tier 2 Emerging Hub"
    },
    "Tier 3 (Jaipur, Lucknow, Indore, Chandigarh, Nagpur)": {
        "cost_multiplier": 0.95,
        "market_land_appreciation_multiplier": 1.15,
        "tier_name": "Tier 3 Growth Center"
    }
}


def calculate_project_valuation(
    structure_type: str,
    built_up_sqft: float,
    location_tier: str,
    completion_percentage: float
) -> CostValuationEstimate:
    """
    Computes CapEx incurred, total budget, material requirements,
    and market asset valuation in INR.
    """
    struct_info = STRUCTURE_RATES.get(
        structure_type, 
        STRUCTURE_RATES["Residential (RCC Frame - Standard)"]
    )
    tier_info = CITY_TIERS.get(
        location_tier,
        CITY_TIERS["Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Chennai)"]
    )

    base_rate = struct_info["base_rate"]
    tier_mult = tier_info["cost_multiplier"]
    effective_rate_per_sqft = base_rate * tier_mult

    total_project_budget = effective_rate_per_sqft * built_up_sqft
    capex_incurred = total_project_budget * (completion_percentage / 100.0)

    # Material quantities
    total_steel_tonnes = (struct_info["steel_per_sqft_kg"] * built_up_sqft) / 1000.0
    total_cement_bags = struct_info["cement_per_sqft_bags"] * built_up_sqft
    total_sand_cft = struct_info["sand_per_sqft_cft"] * built_up_sqft
    total_aggregate_cft = struct_info["aggregate_per_sqft_cft"] * built_up_sqft

    # Market asset valuation accounting for land value premium and development progress
    market_mult = tier_info["market_land_appreciation_multiplier"]
    projected_completed_valuation = total_project_budget * market_mult

    # Current asset valuation based on work completed + initial land/approval equity
    base_land_equity = total_project_budget * 0.35 * market_mult
    current_asset_valuation = base_land_equity + (capex_incurred * 1.22)

    # Determine project milestone
    if completion_percentage < 15:
        milestone = "Site Preparation & Deep Foundation Substructure"
    elif completion_percentage < 35:
        milestone = "RCC Plinth & Lower Floor Framing Superstructure"
    elif completion_percentage < 65:
        milestone = "Mid-Rise Structural Framing & Masonry Infill"
    elif completion_percentage < 85:
        milestone = "MEP Rough-in, Plastering & Waterproofing"
    elif completion_percentage < 99:
        milestone = "Architectural Finishes, Glazing & Fixtures"
    else:
        milestone = "Ready for Occupancy / Handover Audit"

    return CostValuationEstimate(
        structure_type=structure_type,
        built_up_sqft=built_up_sqft,
        location_tier=tier_info["tier_name"],
        city_tier_multiplier=tier_mult,
        completion_percentage=completion_percentage,
        base_rate_per_sqft_inr=round(effective_rate_per_sqft, 2),
        total_project_budget_inr=round(total_project_budget, 2),
        capex_incurred_inr=round(capex_incurred, 2),
        current_asset_valuation_inr=round(current_asset_valuation, 2),
        projected_completed_valuation_inr=round(projected_completed_valuation, 2),
        steel_required_tonnes=round(total_steel_tonnes, 2),
        cement_required_bags=round(total_cement_bags, 0),
        sand_required_cft=round(total_sand_cft, 0),
        aggregates_required_cft=round(total_aggregate_cft, 0),
        timeline_milestone=milestone
    )


def format_inr_currency(amount: float) -> str:
    """Formats an INR amount into readable Lakhs (L) and Crores (Cr)."""
    if amount >= 10000000:  # 1 Crore
        cr_val = amount / 10000000.0
        return f"₹ {cr_val:.2f} Cr"
    elif amount >= 100000:  # 1 Lakh
        lakh_val = amount / 100000.0
        return f"₹ {lakh_val:.2f} Lakhs"
    else:
        return f"₹ {amount:,.2f}"
