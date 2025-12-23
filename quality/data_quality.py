def assess_data_quality(df):
    issues = []
    quality_flags = {}

    # Missing values
    missing_cols = df.columns[df.isnull().any()].tolist()
    if missing_cols:
        issues.append({
            "Type": "Missing Data",
            "Details": f"Missing values in columns: {', '.join(missing_cols)}"
        })

    # Range validation
    if (df["total_co2_kg"] < 0).any():
        issues.append({
            "Type": "Range Violation",
            "Details": "Negative CO₂ values detected"
        })

    # Facility consistency
    facility_variance = df.groupby("facility")["total_co2_kg"].std()
    if (facility_variance > facility_variance.mean() * 2).any():
        issues.append({
            "Type": "Consistency Warning",
            "Details": "Large emissions variance across facilities"
        })

    # Quality flags
    for col in ["scope1_co2_kg", "scope2_co2_kg", "total_co2_kg"]:
        if df[col].isnull().any():
            quality_flags[col] = "Assumed"
        elif "estimated" in col:
            quality_flags[col] = "Estimated"
        else:
            quality_flags[col] = "Measured"

    return {
        "issues": issues,
        "quality_flags": quality_flags
    }
