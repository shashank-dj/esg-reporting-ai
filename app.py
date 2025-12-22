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
    if st.button("📊 ESG Overview", use_container_width=True):
        st.switch_page("pages/1_Overview.py")

    if st.button("📘 Framework Compliance", use_container_width=True):
        st.switch_page("pages/2_Frameworks.py")

with col2:
    if st.button("🛡️ Audit & Risk", use_container_width=True):
        st.switch_page("pages/3_Audit_&_Risk.py")

    if st.button("🌍 Scope 3 Emissions", use_container_width=True):
        st.switch_page("pages/4_Scope_3.py")

with col3:
    if st.button("📈 CSRD Maturity", use_container_width=True):
        st.switch_page("pages/5_Maturity.py")

    if st.button("📄 Reports", use_container_width=True):
        st.switch_page("pages/6_Reports.py")
