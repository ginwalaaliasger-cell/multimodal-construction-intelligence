"""
Structura AI - Multimodal Construction Intelligence Platform
Production-grade enterprise decision-support system for construction planning,
PPE safety compliance, concrete crack diagnostics, valuation & daily operations.
"""

import os
import json
import streamlit as st
from PIL import Image
import pandas as pd

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
from services.cost_estimator import (
    STRUCTURE_RATES,
    CITY_TIERS,
    calculate_project_valuation,
    format_inr_currency
)
from services.weather_advisory import get_weather_advisory, WEATHER_PRESETS
from services.architectural_visualizer import generate_architectural_render_url

# Page configuration
st.set_page_config(
    page_title="Structura AI | Multimodal Construction Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise SaaS CSS
st.markdown("""
<style>
    /* Global Typography & Font Family */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }

    /* Hero Brand Banner */
    .brand-hero {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F2847 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px 30px;
        color: #FFFFFF;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15);
    }
    .brand-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-subtitle {
        font-size: 13.5px;
        color: #94A3B8;
        margin-top: 6px;
        line-height: 1.5;
    }

    /* Metric Cards */
    .saas-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        margin-bottom: 16px;
    }
    .metric-value-highlight {
        font-size: 26px;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.2;
    }
    .metric-label-sub {
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    /* Status Pills */
    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .pill-green {
        background-color: #DCFCE7;
        color: #166534;
        border: 1px solid #BBF7D0;
    }
    .pill-amber {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
    }
    .pill-red {
        background-color: #FEE2E2;
        color: #991B1B;
        border: 1px solid #FECACA;
    }

    /* Section Header */
    .module-header {
        border-left: 4px solid #2563EB;
        padding-left: 12px;
        font-size: 18px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 16px;
        margin-top: 8px;
    }

    /* Safety & Severity Badges */
    .severity-badge-critical {
        background: #DC2626;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }
    .severity-badge-high {
        background: #EA580C;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }
    .severity-badge-medium {
        background: #D97706;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }
    .severity-badge-low {
        background: #059669;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.markdown("### 🏢 Structura AI")
    st.caption("Multimodal Construction Intelligence Decision Support")
    st.markdown("---")

    st.markdown("#### 🔑 Model Authentication")
    gemini_api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        help="Enter your Gemini 1.5/2.0 API key. If left blank, Structura AI automatically operates in Full Enterprise Demonstration Mode.",
        placeholder="AIzaSy..."
    )

    if gemini_api_key.strip():
        st.success("🟢 Gemini Multimodal API Active")
    else:
        st.info("⚡ Enterprise Demonstration Mode Active (Zero API key required)")

    st.markdown("---")
    st.markdown("#### 📐 Architecture & Standards")
    st.markdown("""
    - **Vision LLM:** Gemini 2.5 Flash / Vision
    - **Safety Standard:** OSHA 1926 & IS 3696
    - **Structural Code:** IS 456:2000 & ACI 224R
    - **Economics Engine:** CPWD Indian Indices
    - **Render Engine:** Flux 3D Architectural
    - **Data Integrity:** Strict Pydantic JSON
    """)

    st.markdown("---")
    st.markdown("#### ⚡ 1-Click Sample Loaders")
    load_sample_safety = st.button("📸 Load Sample Site Photo", use_container_width=True)
    load_sample_crack = st.button("🧱 Load Sample Crack Photo", use_container_width=True)

# Hero Header
st.markdown("""
<div class="brand-hero">
    <div class="brand-title">
        <span>🏗️ Structura AI</span>
        <span style="font-size: 14px; font-weight: 500; background: rgba(59, 130, 246, 0.25); color: #93C5FD; padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(147, 197, 253, 0.3);">Enterprise v1.4</span>
    </div>
    <div class="brand-subtitle">
        AI-Powered Multimodal Construction Intelligence Platform for Occupational Safety (OSHA / IS 456), Concrete Defect Diagnostics, Capital Expenditure Planning & Real-Time Operational Advisory.
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🦺 Site Safety & PPE Audit",
    "🔍 Crack Diagnostics & Structural Health",
    "📊 Project Planning & Valuation",
    "🌤️ Weather Advisory & Site Assistant",
    "📄 JSON Data Contracts & API"
])


# ==============================================================================
# TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
# ==============================================================================
with tab1:
    st.markdown('<div class="module-header">Construction Site Safety & PPE Compliance Audit</div>', unsafe_allow_html=True)
    st.caption("Multimodal inspection module auditing worker personal protective equipment against OSHA 1926 and IS 2925/3696 safety standards.")

    col_up, col_preview = st.columns([1, 1])

    uploaded_safety_img = None
    with col_up:
        uploaded_file = st.file_uploader(
            "Upload Construction Site Photo (JPG / PNG)",
            type=["jpg", "jpeg", "png"],
            key="safety_file_uploader"
        )
        if uploaded_file is not None:
            uploaded_safety_img = Image.open(uploaded_file)
        elif load_sample_safety or "sample_safety" in st.session_state:
            st.session_state["sample_safety"] = True
            if os.path.exists("sample_data/site_safety_sample.jpg"):
                uploaded_safety_img = Image.open("sample_data/site_safety_sample.jpg")

        if uploaded_safety_img is not None:
            st.image(uploaded_safety_img, caption="Analyzed Construction Site Image", use_container_width=True)
            run_safety_audit = st.button("🚀 Run Site Safety & PPE Audit", type="primary", use_container_width=True)
        else:
            st.info("👆 Upload an on-site photo or click '📸 Load Sample Site Photo' in the sidebar to begin.")
            run_safety_audit = False

    with col_preview:
        if uploaded_safety_img is not None and run_safety_audit:
            with st.spinner("Analyzing site imagery via Multimodal AI vision model..."):
                audit_data, is_demo = analyze_ppe_safety(uploaded_safety_img, api_key=gemini_api_key)

            st.session_state["last_safety_audit"] = audit_data
            st.session_state["last_safety_demo"] = is_demo

        if "last_safety_audit" in st.session_state:
            audit = st.session_state["last_safety_audit"]
            score = audit.get("safety_score", 0)
            status = audit.get("overall_status", "Needs Attention")

            # Score & Status Display
            status_class = "pill-green" if score >= 85 else ("pill-amber" if score >= 60 else "pill-red")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class="saas-card">
                    <div class="metric-value-highlight">{score}/100</div>
                    <div class="metric-label-sub">Safety Compliance Index</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="saas-card">
                    <div class="metric-value-highlight"><span class="status-pill {status_class}">{status}</span></div>
                    <div class="metric-label-sub">Operational Status</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class="saas-card">
                    <div class="metric-value-highlight">{audit.get('workers_detected', 0)}</div>
                    <div class="metric-label-sub">Workers On-Site</div>
                </div>
                """, unsafe_allow_html=True)

            # PPE Checklist Table
            st.markdown("##### 📋 PPE Equipment Verification Checklist")
            ppe_list = audit.get("ppe_checklist", [])
            if ppe_list:
                df_ppe = pd.DataFrame(ppe_list)
                st.dataframe(
                    df_ppe[["item", "status", "confidence", "notes"]],
                    column_config={
                        "item": "Safety Gear Requirement",
                        "status": "Compliance Status",
                        "confidence": st.column_config.ProgressColumn("Confidence", min_value=0.0, max_value=1.0, format="%.2f"),
                        "notes": "Inspector Notes"
                    },
                    use_container_width=True,
                    hide_index=True
                )

            # Identified Hazards
            st.markdown("##### ⚠️ Detected Site Hazards & Corrective Remedies")
            hazards = audit.get("hazards_identified", [])
            for h in hazards:
                sev = h.get("severity", "Medium")
                badge_class = (
                    "severity-badge-critical" if sev == "Critical"
                    else "severity-badge-high" if sev == "High"
                    else "severity-badge-medium" if sev == "Medium"
                    else "severity-badge-low"
                )
                with st.expander(f"🔴 [{h.get('hazard_id', 'HAZ')}] {h.get('hazard_type', 'Hazard')} — {sev.upper()}", expanded=(sev in ["Critical", "High"])):
                    st.markdown(f"**Observed Condition:** {h.get('description', '')}")
                    st.markdown(f"**Violation Citation:** `{h.get('standard_violated', 'OSHA 1926')}`")
                    st.markdown(f"**Mandatory Corrective Remedy:** {h.get('corrective_remedy', '')}")

            # Download JSON Report
            st.download_button(
                label="📥 Download Structured Audit Report (JSON)",
                data=json.dumps(audit, indent=2),
                file_name=f"Site_Safety_Audit_{audit.get('inspection_timestamp', 'report').replace(' ', '_').replace(':', '-')}.json",
                mime="application/json",
                use_container_width=True
            )


# ==============================================================================
# TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY (EPIC 2)
# ==============================================================================
with tab2:
    st.markdown('<div class="module-header">Concrete Crack Classification & Structural Forensic Diagnostics</div>', unsafe_allow_html=True)
    st.caption("Multimodal structural health monitoring evaluating crack morphology, width (mm), root causes, and repair engineering per IS 456.")

    col_c_up, col_c_preview = st.columns([1, 1])

    uploaded_crack_img = None
    with col_c_up:
        crack_file = st.file_uploader(
            "Upload Concrete / Masonry Surface Photo (JPG / PNG)",
            type=["jpg", "jpeg", "png"],
            key="crack_file_uploader"
        )
        if crack_file is not None:
            uploaded_crack_img = Image.open(crack_file)
        elif load_sample_crack or "sample_crack" in st.session_state:
            st.session_state["sample_crack"] = True
            if os.path.exists("sample_data/crack_sample.jpg"):
                uploaded_crack_img = Image.open("sample_data/crack_sample.jpg")

        if uploaded_crack_img is not None:
            st.image(uploaded_crack_img, caption="Concrete Surface Under Forensic Review", use_container_width=True)
            run_crack_diag = st.button("🔬 Diagnose Structural Defect & Integrity", type="primary", use_container_width=True)
        else:
            st.info("👆 Upload a concrete/wall crack photo or click '🧱 Load Sample Crack Photo' in the sidebar.")
            run_crack_diag = False

    with col_c_preview:
        if uploaded_crack_img is not None and run_crack_diag:
            with st.spinner("Analyzing structural crack morphology and stress trajectories..."):
                crack_data, is_demo = analyze_crack_diagnostics(uploaded_crack_img, api_key=gemini_api_key)
            st.session_state["last_crack_diag"] = crack_data

        if "last_crack_diag" in st.session_state:
            diag = st.session_state["last_crack_diag"]
            defect_type = diag.get("defect_type", "Structural Shear")
            sev = diag.get("severity", "High")
            width_mm = diag.get("estimated_width_mm", 1.5)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class="saas-card">
                    <div class="metric-value-highlight">{defect_type}</div>
                    <div class="metric-label-sub">Defect Classification</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="saas-card">
                    <div class="metric-value-highlight">{width_mm} mm</div>
                    <div class="metric-label-sub">Estimated Aperture</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class="saas-card">
                    <div class="metric-value-highlight"><span class="status-pill pill-red">{sev}</span></div>
                    <div class="metric-label-sub">Structural Severity</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"**Structural Risk Level:** `{diag.get('structural_risk_level', 'High')}`")
            st.markdown(f"**Monitoring Urgency:** `{diag.get('monitoring_urgency', 'Immediate Repair')}`")
            st.info(f"**IS 456 Permissible Compliance:** {diag.get('is456_compliance_notes', 'Exceeds standard 0.3mm tolerance.')}")

            st.markdown("##### 🔎 Probable Root Causes")
            for c in diag.get("probable_root_causes", []):
                st.markdown(f"- {c}")

            st.markdown("##### 🛠️ Recommended Engineering Repairs")
            for r in diag.get("recommended_engineering_repairs", []):
                st.markdown(f"✅ {r}")

            st.markdown(f"**Repair Methodology:** *{diag.get('repair_methodology', '')}*")

            st.download_button(
                label="📥 Download Structural Forensic Report (JSON)",
                data=json.dumps(diag, indent=2),
                file_name="Structural_Crack_Forensics_Report.json",
                mime="application/json",
                use_container_width=True
            )


# ==============================================================================
# TAB 3: PROJECT PLANNING & REAL ESTATE VALUATION (EPIC 3)
# ==============================================================================
with tab3:
    st.markdown('<div class="module-header">Construction Project Planning & Real Estate Valuation (INR)</div>', unsafe_allow_html=True)
    st.caption("Precision civil estimation engine calculating budget, capital expenditure, material procurement quotas, and 3D conceptual architectural renderings.")

    p_col1, p_col2 = st.columns([1, 1])

    with p_col1:
        st.markdown("##### 🏗️ Project Parameters")
        structure_choice = st.selectbox(
            "Structure Classification",
            options=list(STRUCTURE_RATES.keys()),
            index=0
        )
        built_up_sqft = st.number_input(
            "Total Built-up Area (Sq. Ft.)",
            min_value=500,
            max_value=2000000,
            value=25000,
            step=1000
        )
        location_tier = st.selectbox(
            "Location Tier & Regional Cost Index",
            options=list(CITY_TIERS.keys()),
            index=0
        )
        completion_pct = st.slider(
            "Project Completion Stage (%)",
            min_value=0,
            max_value=100,
            value=45,
            step=1
        )

        estimate = calculate_project_valuation(
            structure_type=structure_choice,
            built_up_sqft=built_up_sqft,
            location_tier=location_tier,
            completion_percentage=completion_pct
        )

    with p_col2:
        st.markdown("##### 💰 Financial Valuation & CapEx Metrics")
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""
            <div class="saas-card">
                <div class="metric-value-highlight" style="color: #2563EB;">{format_inr_currency(estimate.total_project_budget_inr)}</div>
                <div class="metric-label-sub">Total Project Budget</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="saas-card">
                <div class="metric-value-highlight">{format_inr_currency(estimate.capex_incurred_inr)}</div>
                <div class="metric-label-sub">CapEx Incurred to Date</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="saas-card">
                <div class="metric-value-highlight" style="color: #059669;">{format_inr_currency(estimate.current_asset_valuation_inr)}</div>
                <div class="metric-label-sub">Current Market Valuation</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="saas-card">
                <div class="metric-value-highlight">{format_inr_currency(estimate.projected_completed_valuation_inr)}</div>
                <div class="metric-label-sub">Projected Completion Value</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"**Current Milestone:** `{estimate.timeline_milestone}`")
        st.progress(estimate.completion_percentage / 100.0)

    st.markdown("---")
    # Material Quantities Breakdown
    st.markdown("##### 🧱 Material Procurement & Quantity Estimation (IS 456 Standards)")
    mat1, mat2, mat3, mat4 = st.columns(4)
    with mat1:
        st.metric("TMT Fe500D Steel", f"{estimate.steel_required_tonnes:,.1f} MT", help="Metric Tonnes of reinforcement steel")
    with mat2:
        st.metric("53-Grade Cement", f"{estimate.cement_required_bags:,.0f} Bags", help="Standard 50kg bags of Portland cement")
    with mat3:
        st.metric("Manufactured Sand", f"{estimate.sand_required_cft:,.0f} CFT", help="Cubic feet of M-Sand")
    with mat4:
        st.metric("Coarse Aggregates", f"{estimate.aggregates_required_cft:,.0f} CFT", help="20mm/10mm graded aggregates")

    st.markdown("---")
    # 3D Architectural Rendering via Pollinations AI Flux
    st.markdown("##### 🏛️ Conceptual 3D Architectural Render (Pollinations AI / Flux)")
    arch_col1, arch_col2 = st.columns([1, 2])
    with arch_col1:
        arch_style = st.selectbox(
            "Architectural Facade Style",
            ["Modern Sustainable Biophilic", "Brutalist Exposed Concrete & Glass", "Neo-Classical Contemporary", "High-Tech Industrial Steel Frame"],
            index=0
        )
        facade_desc = st.text_input(
            "Facade & Material Accent",
            value="Curtain wall glazing, terracotta louvers, and rooftop green terraces"
        )
        gen_render_btn = st.button("🎨 Generate 3D Concept Render", use_container_width=True)

    with arch_col2:
        render_url = generate_architectural_render_url(
            structure_type=structure_choice,
            built_up_sqft=built_up_sqft,
            architectural_style=arch_style,
            facade_material=facade_desc
        )
        if gen_render_btn or "render_active" in st.session_state:
            st.session_state["render_active"] = True
            st.image(render_url, caption=f"3D Architectural Elevation Concept - {structure_choice}", use_container_width=True)
            st.caption(f"⚡ Live Render Generator URL: `{render_url[:80]}...`")
        else:
            st.info("Click 'Generate 3D Concept Render' to stream photorealistic architectural visualization.")


# ==============================================================================
# TAB 4: DAILY SITE ASSISTANT & WEATHER-AWARE ADVISORY (EPIC 5)
# ==============================================================================
with tab4:
    st.markdown('<div class="module-header">Daily Site Assistant & Weather-Aware Safety Advisory</div>', unsafe_allow_html=True)
    st.caption("Dynamic meteorological risk mitigation engine and interactive multi-turn civil engineering assistant.")

    st.markdown("##### 🌦️ Weather Condition Hazard Assessment")
    weather_key = st.selectbox(
        "Active / Projected Weather Forecast",
        options=list(WEATHER_PRESETS.keys()),
        index=0
    )

    advisory = get_weather_advisory(weather_key)

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        st.metric("Ambient Temp", f"{advisory.ambient_temp_c} °C")
    with w2:
        st.metric("Sustained Wind", f"{advisory.wind_speed_kmh} km/h")
    with w3:
        st.metric("Precipitation Risk", f"{advisory.precipitation_prob} %")
    with w4:
        risk_color = "pill-red" if advisory.risk_level in ["Critical", "High"] else "pill-green"
        st.markdown(f"""
        <div style="padding-top: 10px;">
            <div style="font-size: 11px; color: #64748B; font-weight: 600;">SITE RISK RATING</div>
            <span class="status-pill {risk_color}">{advisory.risk_level.upper()}</span>
        </div>
        """, unsafe_allow_html=True)

    # Dynamic Alert Cards
    st.markdown("##### ⚠️ Active Operational Protocols")
    a_col1, a_col2 = st.columns(2)
    with a_col1:
        st.warning(f"🏗️ **Crane & Hoisting:** {advisory.crane_operations}")
        st.info(f"⚡ **Electrical Safety:** {advisory.electrical_safety}")
    with a_col2:
        st.warning(f"🧪 **Concrete Curing & Placement:** {advisory.concrete_curing_advisory}")
        st.info(f"👷 **Worker Shifts & Welfare:** {advisory.worker_shift_adjustments}")

    st.markdown("---")
    st.markdown("##### 💬 Multi-Turn Construction Engineering Assistant")
    
    # Chat message state
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": "Welcome to Structura AI Site Advisory. Ask any civil engineering, OSHA compliance, IS 456 specification, or construction planning questions."
            }
        ]

    # Render history
    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_query = st.chat_input("Enter your civil engineering or safety query (e.g. 'What is the permissible slump for RCC columns under IS 456?')...")
    if user_query:
        st.session_state["chat_messages"].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Consulting construction engineering knowledge base..."):
                resp = get_assistant_chat_response(
                    messages=st.session_state["chat_messages"],
                    api_key=gemini_api_key,
                    current_weather=weather_key
                )
                st.markdown(resp)
        st.session_state["chat_messages"].append({"role": "assistant", "content": resp})


# ==============================================================================
# TAB 5: JSON DATA CONTRACTS & REST SPECIFICATION (EPIC 4)
# ==============================================================================
with tab5:
    st.markdown('<div class="module-header">Strict JSON Data Contracts & REST API Architecture</div>', unsafe_allow_html=True)
    st.caption("Standardized Pydantic schemas guaranteeing zero-breakage data integration between multimodal AI and enterprise frontend services.")

    schema_choice = st.selectbox(
        "Select JSON Schema Contract to Inspect",
        [
            "PPEAuditResult (OSHA / IS 456 Vision Contract)",
            "CrackDiagnosisResult (Structural Forensics Contract)",
            "CostValuationEstimate (Civil Economics Contract)",
            "WeatherSafetyAdvisory (Operational Protocol Contract)"
        ]
    )

    if "PPEAuditResult" in schema_choice:
        st.json(PPEAuditResult.model_json_schema())
    elif "CrackDiagnosisResult" in schema_choice:
        st.json(CrackDiagnosisResult.model_json_schema())
    elif "CostValuationEstimate" in schema_choice:
        st.json(CostValuationEstimate.model_json_schema())
    else:
        st.json(WeatherSafetyAdvisory.model_json_schema())

    st.markdown("##### 🔌 REST API Endpoints Specification")
    st.markdown("""
    | Method | Endpoint | Description |
    | :--- | :--- | :--- |
    | `POST` | `/api/v1/safety/audit-ppe` | Upload site image for multipart OSHA/IS 456 PPE audit |
    | `POST` | `/api/v1/structural/diagnose-crack` | Classify concrete surface defect & get repair methodology |
    | `POST` | `/api/v1/planning/estimate-valuation` | Calculate budget, CapEx, and material metrics |
    | `GET` | `/api/v1/site/weather-advisory` | Fetch weather-contingent safety protocols |
    | `POST` | `/api/v1/assistant/chat` | Multi-turn construction intelligence chat |
    | `GET` | `/api/v1/planning/concept-render` | Stream 3D architectural render via Flux |
    """)
