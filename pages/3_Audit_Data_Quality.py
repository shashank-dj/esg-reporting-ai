import streamlit as st
import pandas as pd

from audit.audit_score import calculate_audit_readiness_score
from explainability.audit_trace import generate_audit_trace
from quality.data_quality import assess_data_quality

# -----------------------------
# Page Title
# -----------------------------
st.title("🛡️ Audit Readiness & Data Quality")

# -----------------------------
# Load Shared Data
# -----------------------------
if "df" not in st.session_state or "kpis" not in st.session_state:
    st.error("❌ ESG data not loaded. Please upload data on the main page.")
    st.stop()

df = st.session_state["df"]
kpis = st.session_state["kpis"]

# -----------------------------
# Audit Readiness
# -----------------------------
audit = calculate_audit_readiness_score(df, kpis)

st.metric(
    label="Audit Readiness Score (0–100)",
    value=audit["total_score"]
)

st.subheader("📋 Audit Score Breakdown")

breakdown_df = pd.DataFrame(
    audit["breakdown"].items(),
    columns=["Assessment Area", "Score Contribution"]
)

st.dataframe(breakdown_df, use_container_width=True)

# -----------------------------
# Audit Explainability
# -----------------------------
trace = generate_audit_trace(df, kpis)

with st.expander("🔍 Explain this audit score"):
    st.json(trace)

# -----------------------------
# Data Quality & Validation
# -----------------------------
st.subheader("🧪 Data Quality & Validation")

quality = assess_data_quality(df)

if quality["issues"]:
    st.warning("⚠️ Data quality issues detected")
    st.dataframe(
        pd.DataFrame(quality["issues"]),
        use_container_width=True
    )
else:
    st.success("✅ No major data quality issues detected")

# -----------------------------
# Data Quality Flags
# -----------------------------
st.subheader("🏷️ Data Quality Flags (Audit-Relevant)")

flags_df = pd.DataFrame(
    quality["quality_flags"].items(),
    columns=["Metric", "Quality Classification"]
)

st.dataframe(flags_df, use_container_width=True)

st.caption(
    "Measured = Directly captured | Estimated = Model-based | "
    "Assumed = Incomplete or inferred data"
)
