import streamlit as st
import pandas as pd
from esg.emissions import calculate_emissions, aggregate_kpis
from audit.audit_score import calculate_audit_readiness_score
from explainability.audit_trace import generate_audit_trace

st.title("🛡️ Audit Readiness & Risk")

df = calculate_emissions(pd.read_csv("data/sample_company_data.csv"))
kpis = aggregate_kpis(df)

audit = calculate_audit_readiness_score(df, kpis)
st.metric("Audit Readiness Score", audit["total_score"])

trace = generate_audit_trace(df, kpis)
with st.expander("🔍 Explain this score"):
    st.json(trace)
