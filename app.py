import streamlit as st
import pandas as pd
import plotly.express as px

from esg.emissions import calculate_emissions, aggregate_kpis
from reports.pdf_report import generate_esg_pdf

st.set_page_config(page_title="ESG Reporting MVP", layout="wide")

st.title("🌱 ESG Reporting Software – MVP")
st.caption("Environmental Metrics • CO₂ Accounting • Sustainability Intelligence")

# -----------------------------
# Load Data
# -----------------------------
uploaded_file = st.file_uploader("Upload ESG Data (CSV)", type="csv")

if uploaded_file:
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
col2.metric("Renewable (%)", kpis["Renewable Energy (%)"])
col3.metric("Scope 1 CO₂ (kg)", kpis["Scope 1 CO₂ (kg)"])
col4.metric("Scope 2 CO₂ (kg)", kpis["Scope 2 CO₂ (kg)"])
col5.metric("Total CO₂ (kg)", kpis["Total CO₂ (kg)"])

# -----------------------------
# Charts
# -----------------------------
st.subheader("📈 Emissions Trend")

df["date"] = pd.to_datetime(df["date"])
trend = df.groupby("date")["total_co2_kg"].sum().reset_index()

fig = px.line(
    trend,
    x="date",
    y="total_co2_kg",
    title="Daily CO₂ Emissions Trend (kg)"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("📄 ESG Report")

pdf_bytes = generate_esg_pdf(kpis)

st.download_button(
    label="⬇️ Download ESG Report (PDF)",
    data=pdf_bytes,
    file_name="esg_environmental_report.pdf",
    mime="application/pdf",
)


# -----------------------------
# Facility Breakdown
# -----------------------------
st.subheader("🏭 Facility-wise Emissions")

facility_fig = px.bar(
    df.groupby("facility")["total_co2_kg"].sum().reset_index(),
    x="facility",
    y="total_co2_kg",
    title="CO₂ Emissions by Facility"
)

st.plotly_chart(facility_fig, use_container_width=True)

# -----------------------------
# Raw Data
# -----------------------------
with st.expander("🔍 View Raw ESG Data"):
    st.dataframe(df)
