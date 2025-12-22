import streamlit as st

st.set_page_config(
    page_title="ESG Reporting Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🌱 ESG Reporting Platform")
st.caption("Enterprise ESG Reporting • CSRD Compliance • Audit Intelligence")

st.markdown(
    """
This platform helps organizations measure, assess, and report ESG performance
with a strong focus on **CSRD compliance**, **audit readiness**, and **decision transparency**.
"""
)

st.divider()

st.subheader("🚀 Select a module to explore")

module = st.radio(
    "Choose a section",
    [
        "📊 ESG Overview",
        "📘 Framework Compliance",
        "🛡️ Audit & Risk",
        "🌍 Scope 3 Emissions",
        "📈 CSRD Maturity",
        "📄 Reports & Downloads",
    ],
)

st.divider()

if st.button("➡️ Open selected module", use_container_width=True):
    if module == "📊 ESG Overview":
        st.switch_page("pages/1_Overview.py")

    elif module == "📘 Framework Compliance":
        st.switch_page("pages/2_Frameworks.py")

    elif module == "🛡️ Audit & Risk":
        st.switch_page("pages/3_Audit_Risk.py")

    elif module == "🌍 Scope 3 Emissions":
        st.switch_page("pages/4_Scope_3.py")

    elif module == "📈 CSRD Maturity":
        st.switch_page("pages/5_Maturity.py")

    elif module == "📄 Reports & Downloads":
        st.switch_page("pages/6_Reports.py")

st.info("💡 You can also navigate directly using the sidebar on the left.")
