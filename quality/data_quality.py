"""
Data Quality & Validation Layer
Audit-safe, schema-tolerant ESG data quality checks
"""

def assess_data_quality(df):
    issues = []
    quality_flags = {}

    # -----------------------------
    # 1. Missing Data Check
    # -----------------------------
    missing_cols = [col for col in df.columns if df[col].isnull().any()]
    if missing_cols:
        issues.append({
            "Type": "Missing Data",
            "Details": f"Missing values detected in columns: {', '.join(missing_cols)}"
        })

    # -----------------------------
    # 2. Range Validation (only if column exists)
    # -----------------------------
    if "total_co2_kg" in df.columns:
        if (df["total_co2_kg"] < 0).any():
            issues.append({
                "Type": "Range Violation",
                "Details": "Negative CO₂ emission values detected"
            })

    # -----------------------------
    # 3. Facility Consistency Check
    # -----------------------------
    if "facility" in df.columns and "total_co2_kg" in df.columns:
        facility_variance = df.groupby("facility")["total_co2_kg"].std()
        if facility_variance.notna().any():
            if (facility_variance > facility_variance.mean() * 2).any():
                issues.append({
                    "Type": "Consistency Warning",
                    "Details": "Large emission variance detected across facilities"
                })

    # -----------------------------
    # 4. Data Quality Flags (Schema-safe)
    # -----------------------------
    expected_metrics = [
        "scope1_co2_kg",
        "scope2_co2_kg",
        "total_co2_kg",
        "energy_kwh"
    ]

    for metric in expected_metrics:
        if metric not in df.columns:
            quality_flags[metric] = "Assumed"
        elif df[metric].isnull().any():
            quality_flags[metric] = "Estimated"
        else:
            quality_flags[metric] = "Measured"

    return {
        "issues": issues,
        "quality_flags": quality_flags
    }
