import streamlit as st
from reports.narrative_builder import generate_esg_narrative

st.title("📖 ESG Narrative & Disclosure")

kpis = st.session_state["kpis"]
audit_score = st.session_state["audit_score"]
maturity = st.session_state["maturity"]

narrative = generate_esg_narrative(kpis, audit_score, maturity)

for section, text in narrative.items():
    st.subheader(section)
    st.write(text)
