import streamlit as st

st.set_page_config(
    page_title="ESG Reporting Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌱 ESG Reporting Platform")
st.caption("Enterprise ESG Reporting • CSRD Compliance • Audit Intelligence")

st.markdown("### Explore the platform")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link(
        "pages/1_Overview.py",
        label="📊 ESG Overview",
        help="Operational ESG metrics and emissions overview"
    )

    st.page_link(
        "pages/2_Frameworks.py",
        label="📘 Framework Compliance",
        help="CSRD, GRI, SASB, TCFD mappings"
    )

with col2:
    st.page_link(
        "pages/3_Audit_&_Risk.py",
        label="🛡️ Audit & Risk",
        help="Audit readiness score and explainability"
    )

    st.page_link(
        "pages/4_Scope_3.py",
        label="🌍 Scope 3 Emissions",
        help="Supplier-based Scope 3 estimation"
    )

with col3:
    st.page_link(
        "pages/5_Maturity.py",
        label="📈 CSRD Maturity",
        help="CSRD maturity assessment by year"
    )

    st.page_link(
        "pages/6_Reports.py",
        label="📄 Reports",
        help="Download ESG and CSRD reports"
    )
