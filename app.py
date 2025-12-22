import streamlit as st
import pandas as pd
import plotly.express as px

from esg.emissions import calculate_emissions, aggregate_kpis
from reports.pdf_report import generate_esg_pdf
from frameworks.csrd_gri_mapping import get_csrd_gri_mapping
from audit.audit_score import calculate_audit_readiness_score
from reports.csrd_gap_analysis import generate_csrd_gap_pdf
from esg.scope3 import estimate_scope3_emissions, aggregate_scope3_kpi
from audit.csrd_maturity import calculate_csrd_maturity
from datetime import datetime

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="ESG Reporting MVP",
    layout="wide",
)

st.title("🌱 ESG Reporting Software – MVP")
st.caption("Environmental Metrics • CO₂ Accounting • Sustainability Intelligence")

# -----------------------------
# Load Data
# -----------------------------
st.subheader("📂 Data Input")

uploaded_file = st.file_uploader(
    "Upload ESG Data (CSV)",
    type="csv"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/sample_company_data.csv")

# -----------------------------
# ESG Calculations
# -----------------------------
df = calculate_emissions(df)
kpis = aggregate_kpis(df)

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("📊 Key ESG Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Energy (kWh)", kpis["Total Energy (kWh)"])
col2.metric("Renewable (%)", f"{kpis['Renewable Energy (%)']}%")
col3.metric("Scope 1 CO₂ (kg)", kpis["Scope 1 CO₂ (kg)"])
col4.metric("Scope 2 CO₂ (kg)", kpis["Scope 2 CO₂ (kg)"])
col5.metric("Total CO₂ (kg)", kpis["Total CO₂ (kg)"])

# -----------------------------
# Emissions Trend
# -----------------------------
st.subheader("📈 Emissions Trend")

df["date"] = pd.to_datetime(df["date"])

trend_df = (
    df.groupby("date", as_index=False)["total_co2_kg"]
    .sum()
)

trend_fig = px.line(
    trend_df,
    x="date",
    y="total_co2_kg",
    title="Daily CO₂ Emissions Trend (kg)"
)

st.plotly_chart(trend_fig, use_container_width=True)

# -----------------------------
# Facility-wise Emissions
# -----------------------------
st.subheader("🏭 Facility-wise Emissions")

facility_df = (
    df.groupby("facility", as_index=False)["total_co2_kg"]
    .sum()
)

facility_fig = px.bar(
    facility_df,
    x="facility",
    y="total_co2_kg",
    title="CO₂ Emissions by Facility",
)

st.plotly_chart(facility_fig, use_container_width=True)

# -----------------------------
# CSRD / GRI Compliance Mapping
# -----------------------------
st.subheader("📘 CSRD / GRI Framework Mapping")

mapping_data = get_csrd_gri_mapping()
mapping_df = pd.DataFrame(mapping_data)

st.dataframe(
    mapping_df,
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "This table maps calculated ESG metrics to CSRD (ESRS) and GRI disclosure requirements."
)

# -----------------------------
# Audit Readiness Score
# -----------------------------
st.subheader("🛡️ ESG Audit Readiness Score")

audit_result = calculate_audit_readiness_score(df, kpis)

score = audit_result["total_score"]
breakdown = audit_result["breakdown"]

if score >= 80:
    status = "🟢 Audit Ready"
elif score >= 50:
    status = "🟡 Partially Ready"
else:
    status = "🔴 High Risk"

st.metric(
    label="Overall Audit Readiness (0–100)",
    value=score,
    delta=status,
)

breakdown_df = pd.DataFrame(
    breakdown.items(),
    columns=["Assessment Area", "Score Contribution"]
)

st.dataframe(
    breakdown_df,
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Audit readiness is calculated based on data completeness, emissions coverage, renewable transparency, and CSRD/GRI alignment."
)

# -----------------------------
# Raw Data Viewer
# -----------------------------
with st.expander("🔍 View Raw ESG Data"):
    st.dataframe(df)
# -----------------------------
# CSRD Gap Analysis Report
# -----------------------------
st.subheader("📑 CSRD Gap Analysis")

csrd_pdf_bytes = generate_csrd_gap_pdf(
    kpis=kpis,
    audit_score=score
)

st.download_button(
    label="⬇️ Download CSRD Gap Analysis (PDF)",
    data=csrd_pdf_bytes,
    file_name="csrd_gap_analysis_report.pdf",
    mime="application/pdf",
)
# -----------------------------
# Scope 3 Emissions (Estimated)
# -----------------------------
st.subheader("🌍 Scope 3 Emissions (Estimated)")

scope3_file = st.file_uploader(
    "Upload Scope 3 Spend Data (CSV)",
    type="csv",
    key="scope3"
)

if scope3_file is not None:
    scope3_df = pd.read_csv(scope3_file)
else:
    scope3_df = pd.read_csv("data/sample_scope3_spend.csv")

scope3_result = estimate_scope3_emissions(scope3_df)
scope3_total = aggregate_scope3_kpi(scope3_result)

st.metric(
    "Estimated Scope 3 CO₂ (kg)",
    scope3_total
)

st.dataframe(scope3_result, use_container_width=True)

st.caption(
    "Scope 3 emissions are estimated using a spend-based methodology "
    "(CSRD-acceptable for early maturity stages)."
)
# -----------------------------
# CSRD Maturity Scoring by Year
# -----------------------------
st.subheader("📈 CSRD Maturity Scoring")

current_year = datetime.now().year
scope3_present = scope3_total > 0

maturity = calculate_csrd_maturity(
    year=current_year,
    audit_score=score,
    scope3_present=scope3_present
)

st.metric(
    "CSRD Maturity Level",
    f"Level {maturity['maturity_level']} – {maturity['maturity_label']}"
)

maturity_df = pd.DataFrame([maturity])
st.dataframe(maturity_df, use_container_width=True)

# -----------------------------
# ESG Report Download (END)
# -----------------------------
st.subheader("📄 Download ESG Report")

pdf_bytes = generate_esg_pdf(kpis)

st.download_button(
    label="⬇️ Download ESG Environmental Report (PDF)",
    data=pdf_bytes,
    file_name="esg_environmental_report.pdf",
    mime="application/pdf",
)
