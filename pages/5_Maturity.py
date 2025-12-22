import streamlit as st
import pandas as pd
from audit.csrd_maturity import calculate_csrd_maturity
from datetime import datetime

st.title("📈 CSRD Maturity")

maturity = calculate_csrd_maturity(
    year=datetime.now().year,
    audit_score=63,
    scope3_present=True
)

st.metric(
    "CSRD Maturity Level",
    f"Level {maturity['maturity_level']} – {maturity['maturity_label']}"
)

st.dataframe(pd.DataFrame([maturity]))
