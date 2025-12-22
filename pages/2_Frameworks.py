import streamlit as st
import pandas as pd
from frameworks.framework_registry import get_all_framework_mappings
from frameworks.framework_coverage import get_framework_coverage

st.title("📘 ESG Framework Compliance")

frameworks = get_all_framework_mappings()
selected = st.selectbox("Select Framework", list(frameworks.keys()))
st.dataframe(pd.DataFrame(frameworks[selected]), use_container_width=True)

st.subheader("🧩 Framework Coverage Heatmap")
st.dataframe(pd.DataFrame(get_framework_coverage()), use_container_width=True)
