import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from esg.emissions import calculate_emissions, aggregate_kpis
from esg.scope3 import estimate_scope3_emissions, aggregate_scope3_kpi
from audit.audit_score import calculate_audit_readiness_score
from audit.csrd_maturity import calculate_csrd_maturity
from frameworks.framework_registry import get_all_framework_mappings
from frameworks.framework_coverage import get_framework_coverage
from explainability.audit_trace import generate_audit_trace
from reports.pdf_report import generate_esg_pdf
from reports.csrd_gap_analysis import generate_csrd_gap_pdf
from finance.esg_finance_mapping import get_esg_financial_linkage

# -----------------------------
# Helper: Financial Signal Formatter
# -----------------------------
def format_financial_signal(signal: str) -> str:
    if signal in ["High", "Weak"]:
        return f"🔴 {signal}"
    elif signal in ["Moderate", "Improving"]:
        return f"🟡 {signal}"
    elif signal in ["Low"]:
        return f"🟢 {signal}"
    return signal

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="ESG Reporting Platform",
    layout="wide",
)

st.title("🌱 ESG Reporting Platform")
st.caption("Enterprise ESG Reporting • CSRD Compliance • Audit Intelligence")

# -----------------------------
# Load Data (Shared Across Tabs)
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

df = calculate_emissions(df)
kpis = aggregate_kpis(df)

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview",
    "📘 Frameworks",
    "🛡️ Audit & Risk",
    "🌍 Scope 3",
    "📈 CSRD Maturity",
    "📄 Reports",
    "💰 ESG → Financial Impact",
])

# -----------------------------
# TAB 1: Overview
# -----------------------------
with tab1:
    st.subheader("📊 Key ESG Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Energy (kWh)", kpis["Total Energy (kWh)"])
    col2.metric("Renewable (%)", f"{kpis['Renewable Energy (%)']}%")
    col3.metric("Scope 1 CO₂ (kg)", kpis["Scope 1 CO₂ (kg)"])
    col4.metric("Scope 2 CO₂ (kg)", kpis["Scope 2 CO₂ (kg)"])
    col5.metric("Total CO₂ (kg)", kpis["Total CO₂ (kg)"])

    df["date"] = pd.to_datetime(df["date"])
    trend_df = df.groupby("date", as_index=False)["total_co2_kg"].sum()

    fig = px.line(trend_df, x="date", y="total_co2_kg", title="CO₂ Emissions Trend")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TAB 2: Frameworks
# -----------------------------
with tab2:
    st.subheader("📘 ESG Framework Compliance")

    frameworks = get_all_framework_mappings()
    selected = st.selectbox("Select Framework", list(frameworks.keys()))
    st.dataframe(pd.DataFrame(frameworks[selected]), use_container_width=True)

    st.subheader("🧩 Framework Coverage Heatmap")
    st.dataframe(pd.DataFrame(get_framework_coverage()), use_container_width=True)

# -----------------------------
# TAB 3: Audit & Risk
# -----------------------------
with tab3:
    st.subheader("🛡️ Audit Readiness Score")

    audit = calculate_audit_readiness_score(df, kpis)
    score = audit["total_score"]

    st.metric("Audit Readiness (0–100)", score)

    breakdown_df = pd.DataFrame(
        audit["breakdown"].items(),
        columns=["Area", "Score Contribution"]
    )
    st.dataframe(breakdown_df, use_container_width=True)

    audit_trace = generate_audit_trace(df, kpis)
    with st.expander("🔍 Explain this score"):
        st.json(audit_trace)

# -----------------------------
# TAB 4: Scope 3
# -----------------------------
with tab4:
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

    st.metric("Estimated Scope 3 CO₂ (kg)", scope3_total)
    st.dataframe(scope3_result, use_container_width=True)

# -----------------------------
# TAB 5: CSRD Maturity
# -----------------------------
with tab5:
    st.subheader("📈 CSRD Maturity Scoring")

    maturity = calculate_csrd_maturity(
        year=datetime.now().year,
        audit_score=score,
        scope3_present=scope3_total > 0
    )

    st.metric(
        "CSRD Maturity Level",
        f"Level {maturity['maturity_level']} – {maturity['maturity_label']}"
    )

    st.dataframe(pd.DataFrame([maturity]), use_container_width=True)

# -----------------------------
# TAB 6: Reports
# -----------------------------
with tab6:
    st.subheader("📄 Download Reports")

    st.download_button(
        "⬇️ ESG Environmental Report",
        generate_esg_pdf(kpis),
        file_name="esg_environmental_report.pdf",
        mime="application/pdf",
    )

    st.download_button(
        "⬇️ CSRD Gap Analysis Report",
        generate_csrd_gap_pdf(kpis, score),
        file_name="csrd_gap_analysis_report.pdf",
        mime="application/pdf",
    )

# -----------------------------
# TAB 7: ESG → Financial Impact
# -----------------------------
with tab7:
    st.subheader("💰 ESG → Financial Impact")

    st.markdown(
        """
        This view translates ESG performance into **financial risk and value signals**.
        Insights are **directional**, designed for **executive and CFO decision-making**.
        """
    )

    # ESG → Finance linkage
    finance_insights = get_esg_financial_linkage(
        kpis=kpis,
        audit_score=score,
        maturity_level=maturity["maturity_level"]
    )

    finance_df = pd.DataFrame(finance_insights)
    finance_df["Financial Signal"] = finance_df["Financial Signal"].apply(format_financial_signal)

    st.dataframe(
        finance_df,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # CFO Summary
    # -----------------------------
    st.divider()

    high_risk = finance_df["Financial Signal"].str.contains("🔴").sum()
    moderate_risk = finance_df["Financial Signal"].str.contains("🟡").sum()

    if high_risk > 0:
        st.error(
            f"💼 CFO Summary: {high_risk} ESG drivers present **elevated financial risk** "
            "and should be prioritized for mitigation."
        )
    elif moderate_risk > 0:
        st.warning(
            "💼 CFO Summary: ESG performance shows **moderate financial exposure** "
            "with opportunities for cost and risk optimization."
        )
    else:
        st.success(
            "💼 CFO Summary: ESG performance indicates **low financial risk** "
            "and supports long-term value stability."
        )

    # -----------------------------
    # ESG Decision Path
    # -----------------------------
    st.subheader("🔗 ESG Decision Path")

    st.markdown(
        """
        **Renewable Energy Usage ↑**  
        → Energy Cost Volatility ↓  
        → Operating Cost Stability ↑  
        → Audit Readiness ↑  
        → CSRD Maturity ↑  
        """
    )

    st.info(
        "🎯 Demo Insight: Improving renewable energy sourcing delivers the strongest "
        "combined ESG and financial impact across cost stability, audit readiness, "
        "and regulatory risk."
    )
