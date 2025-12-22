import streamlit as st
import pandas as pd
import plotly.express as px
from esg.emissions import calculate_emissions, aggregate_kpis

st.title("📊 ESG Overview")

df = pd.read_csv("data/sample_company_data.csv")
df = calculate_emissions(df)
kpis = aggregate_kpis(df)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Energy (kWh)", kpis["Total Energy (kWh)"])
col2.metric("Renewable (%)", f"{kpis['Renewable Energy (%)']}%")
col3.metric("Scope 1 CO₂ (kg)", kpis["Scope 1 CO₂ (kg)"])
col4.metric("Scope 2 CO₂ (kg)", kpis["Scope 2 CO₂ (kg)"])
col5.metric("Total CO₂ (kg)", kpis["Total CO₂ (kg)"])

df["date"] = pd.to_datetime(df["date"])
trend_df = df.groupby("date", as_index=False)["total_co2_kg"].sum()

fig = px.line(trend_df, x="date", y="total_co2_kg")
st.plotly_chart(fig, use_container_width=True)
