import os
import streamlit as st

st.write("OPENAI key loaded:", bool(os.getenv("OPENAI_API_KEY")))

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from esg.emissions import calculate_emissions, aggregate_kpis
from esg.scope3 import estimate_scope3_emissions, aggregate_scope3_kpi
from audit.audit_score import calculate_audit_readiness_score
from audit.csrd_maturity import calculate_csrd_maturity
from frameworks.framework_registry import get_all_framework_mappings
from frameworks.framework_coverage import get_framework_coverage
from explainability.audit_trace import generate_audit_trace
from reports.pdf_report import generate_esg_pdf
from reports.csrd_gap_analysis import generate_csrd_gap_pdf
from finance.esg_finance_mapping import get_esg_financial_linkage

from quality.data_quality import assess_data_quality
from reports.narrative_builder import generate_esg_narrative
from versioning.period_comparison import compare_periods

from ai.esg_narrative_copilot import build_esg_context, generate_ai_narrative
from ai.llm_client import OpenAILLMClient

# -----------------------------
# Helper: Financial Signal Formatter
# -----------------------------
def format_financial_signal(signal: str) -> str:
    if signal in ["High", "Weak"]:
        return f"🔴 {signal}"
    elif signal in ["Moderate", "Improving"]:
        return f"🟡 {signal}"
    elif signal in ["Low"]:
        return f"🟢 {signal}"
    return signal

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="ESG Reporting Platform",
    layout="wide",
)

st.title("🌱 ESG Reporting Platform")
st.caption("Enterprise ESG Reporting • CSRD Compliance • Audit Intelligence")

# -----------------------------
# Load Data
# -----------------------------
st.subheader("📂 Data Input")

uploaded_file = st.file_uploader("Upload ESG Data (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/sample_company_data.csv")

# -----------------------------
# Core ESG Calculations
# -----------------------------
df = calculate_emissions(df)
kpis = aggregate_kpis(df)

audit = calculate_audit_readiness_score(df, kpis)
score = audit["total_score"]

quality_result = assess_data_quality(df)

scope3_present = False

# -----------------------------
# CSRD Maturity (needed by multiple tabs/pages)
# -----------------------------
maturity = calculate_csrd_maturity(
    year=datetime.now().year,
    audit_score=score,
    scope3_present=False,  # updated later if scope 3 is loaded
)

# -----------------------------
# 🔑 STORE SHARED STATE (CRITICAL FOR PAGES)
# -----------------------------
st.session_state["df"] = df
st.session_state["kpis"] = kpis
st.session_state["audit_score"] = score
st.session_state["audit"] = audit
st.session_state["quality"] = quality_result
st.session_state["maturity"] = maturity

# -----------------------------
# Tabs (Demo / Overview Mode)
# -----------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Overview",
    "📘 Frameworks",
    "🛡️ Audit & Data Quality",
    "🌍 Scope 3",
    "📈 CSRD Maturity",
    "📖 ESG Narrative",
    "💰 ESG → Financial Impact",
    "📄 Reports & Versioning",
])

# -----------------------------
# TAB 1: Overview
# -----------------------------
with tab1:
    st.subheader("📊 Key ESG Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Energy (kWh)", kpis["Total Energy (kWh)"])
    col2.metric("Renewable (%)", f"{kpis['Renewable Energy (%)']}%")
    col3.metric("Scope 1 CO₂ (kg)", kpis["Scope 1 CO₂ (kg)"])
    col4.metric("Scope 2 CO₂ (kg)", kpis["Scope 2 CO₂ (kg)"])
    col5.metric("Total CO₂ (kg)", kpis["Total CO₂ (kg)"])

    df["date"] = pd.to_datetime(df["date"])
    trend_df = df.groupby("date", as_index=False)["total_co2_kg"].sum()

    fig = px.line(trend_df, x="date", y="total_co2_kg", title="CO₂ Emissions Trend")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TAB 2: Frameworks
# -----------------------------
with tab2:
    st.subheader("📘 ESG Framework Compliance")

    frameworks = get_all_framework_mappings()
    selected = st.selectbox("Select Framework", list(frameworks.keys()))
    st.dataframe(pd.DataFrame(frameworks[selected]), use_container_width=True)

    st.subheader("🧩 Framework Coverage Heatmap")
    st.dataframe(pd.DataFrame(get_framework_coverage()), use_container_width=True)

# -----------------------------
# TAB 3: Audit & Data Quality
# -----------------------------
with tab3:
    st.subheader("🛡️ Audit Readiness Score")

    st.metric("Audit Readiness (0–100)", score)

    st.dataframe(
        pd.DataFrame(audit["breakdown"].items(), columns=["Area", "Score Contribution"]),
        use_container_width=True,
    )

    with st.expander("🔍 Audit Explainability"):
        st.json(generate_audit_trace(df, kpis))

    st.subheader("📋 Data Quality & Validation")

    if quality_result["issues"]:
        st.warning("Data quality issues detected")
        st.dataframe(pd.DataFrame(quality_result["issues"]), use_container_width=True)
    else:
        st.success("No major data quality issues detected")

    flags_df = pd.DataFrame(
        quality_result["quality_flags"].items(),
        columns=["Metric", "Quality Flag"]
    )
    st.dataframe(flags_df, use_container_width=True)

# -----------------------------
# TAB 4: Scope 3
# -----------------------------
with tab4:
    st.subheader("🌍 Scope 3 Emissions (Estimated)")

    scope3_file = st.file_uploader(
        "Upload Scope 3 Spend Data (CSV)",
        type="csv",
        key="scope3"
    )

    if scope3_file is not None:
        scope3_df = pd.read_csv(scope3_file)
        scope3_result = estimate_scope3_emissions(scope3_df)
        scope3_total = aggregate_scope3_kpi(scope3_result)
        scope3_present = scope3_total > 0

        st.metric("Estimated Scope 3 CO₂ (kg)", scope3_total)
        st.dataframe(scope3_result, use_container_width=True)

        # Update maturity once scope 3 is known
        maturity = calculate_csrd_maturity(
            year=datetime.now().year,
            audit_score=score,
            scope3_present=scope3_present,
        )
        st.session_state["maturity"] = maturity

# -----------------------------
# TAB 5: CSRD Maturity
# -----------------------------
with tab5:
    st.metric(
        "CSRD Maturity Level",
        f"Level {maturity['maturity_level']} – {maturity['maturity_label']}",
    )

    st.dataframe(pd.DataFrame([maturity]), use_container_width=True)

# -----------------------------
# TAB 6: ESG Narrative
# -----------------------------
with tab6:
    st.subheader("📖 ESG Narrative & Disclosure")

    use_ai = st.toggle("🤖 Use AI Narrative Copilot")

    if use_ai:
        llm = OpenAILLMClient()

        context = build_esg_context(
            kpis=kpis,
            audit=st.session_state["audit"],
            maturity=maturity,
            data_quality=st.session_state["quality"]
        )

        with st.spinner("Generating AI-powered ESG narrative..."):
            ai_text = generate_ai_narrative(context, llm)

        st.markdown(ai_text)

        st.caption(
            "AI-generated narrative grounded strictly in reported ESG data. "
            "No external assumptions applied."
        )

    else:
        narrative = generate_esg_narrative(kpis, score, maturity)
        for section, text in narrative.items():
            st.markdown(f"### {section}")
            st.write(text)


# -----------------------------
# TAB 7: ESG → Financial Impact
# -----------------------------
with tab7:
    st.subheader("💰 ESG → Financial Impact")

    finance_insights = get_esg_financial_linkage(
        kpis=kpis,
        audit_score=score,
        maturity_level=maturity["maturity_level"],
    )

    finance_df = pd.DataFrame(finance_insights)
    finance_df["Financial Signal"] = finance_df["Financial Signal"].apply(format_financial_signal)

    st.dataframe(finance_df, use_container_width=True, hide_index=True)

# -----------------------------
# TAB 8: Reports & Versioning
# -----------------------------
with tab8:
    st.subheader("📄 Reports")

    st.download_button(
        "⬇️ ESG Environmental Report",
        generate_esg_pdf(kpis),
        file_name="esg_environmental_report.pdf",
        mime="application/pdf",
    )

    st.download_button(
        "⬇️ CSRD Gap Analysis Report",
        generate_csrd_gap_pdf(kpis, score),
        file_name="csrd_gap_analysis_report.pdf",
        mime="application/pdf",
    )

    st.subheader("📅 Year-over-Year Comparison")

    previous_kpis = {
        "Total CO₂ (kg)": kpis["Total CO₂ (kg)"] * 1.1,
        "Renewable Energy (%)": max(0, kpis["Renewable Energy (%)"] - 5),
    }

    comparison = compare_periods(kpis, previous_kpis)
    st.dataframe(pd.DataFrame(comparison), use_container_width=True)
