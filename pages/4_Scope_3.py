import streamlit as st
import pandas as pd
from esg.scope3 import estimate_scope3_emissions, aggregate_scope3_kpi

st.title("🌍 Scope 3 Emissions")

df = pd.read_csv("data/sample_scope3_spend.csv")
result = estimate_scope3_emissions(df)
st.metric("Estimated Scope 3 CO₂ (kg)", aggregate_scope3_kpi(result))
st.dataframe(result)
