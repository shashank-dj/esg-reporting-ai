import streamlit as st
import pandas as pd

from reports.pdf_report import generate_esg_pdf
from reports.csrd_gap_analysis import generate_csrd_gap_pdf
from versioning.period_comparison import compare_periods

st.title("📄 Reports & Versioning")

kpis = st.session_state["kpis"]
audit_score = st.session_state["audit_score"]

st.subheader("📥 Report Downloads")

st.download_button(
    "⬇️ ESG Environmental Report",
    generate_esg_pdf(kpis),
    file_name="esg_environmental_report.pdf",
)

st.download_button(
    "⬇️ CSRD Gap Analysis Report",
    generate_csrd_gap_pdf(kpis, audit_score),
    file_name="csrd_gap_analysis_report.pdf",
)

st.subheader("📅 Year-over-Year Comparison")

previous_kpis = {
    "Total CO₂ (kg)": kpis["Total CO₂ (kg)"] * 1.1,
    "Renewable Energy (%)": max(0, kpis["Renewable Energy (%)"] - 5),
}

comparison = compare_periods(kpis, previous_kpis)
st.dataframe(pd.DataFrame(comparison))
