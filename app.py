import streamlit as st
import pandas as pd
import plotly.express as px

from esg.emissions import calculate_emissions, aggregate_kpis
from reports.pdf_report import generate_esg_pdf
from frameworks.csrd_gri_mapping import get_csrd_gri_mapping

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
# ESG Report Download
# -----------------------------
st.subheader("📄 ESG Report")

pdf_bytes = generate_esg_pdf(kpis)

st.download_button(
    label="⬇️ Download ESG Report (PDF)",
    data=pdf_bytes,
    file_name="esg_environmental_report.pdf",
    mime="application/pdf",
)

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
# Raw Data Viewer
# -----------------------------
with st.expander("🔍 View Raw ESG Data"):
    st.dataframe(df)
