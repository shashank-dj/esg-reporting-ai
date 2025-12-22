import streamlit as st
from reports.pdf_report import generate_esg_pdf
from reports.csrd_gap_analysis import generate_csrd_gap_pdf

st.title("📄 Reports & Downloads")

st.download_button(
    "⬇️ ESG Environmental Report",
    generate_esg_pdf({}),
    "esg_report.pdf"
)

st.download_button(
    "⬇️ CSRD Gap Analysis Report",
    generate_csrd_gap_pdf({}, 63),
    "csrd_gap.pdf"
)
