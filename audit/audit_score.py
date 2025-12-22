import pandas as pd


def calculate_audit_readiness_score(df: pd.DataFrame, kpis: dict) -> dict:
    score = 0
    breakdown = {}

    # -----------------------------
    # 1. Data Completeness (30)
    # -----------------------------
    required_columns = [
        "date",
        "facility",
        "energy_kwh",
        "renewable_kwh",
        "fuel_liters",
    ]

    missing_cols = [c for c in required_columns if c not in df.columns]

    if not missing_cols:
        completeness_score = 30
    else:
        completeness_score = max(0, 30 - (len(missing_cols) * 6))

    breakdown["Data Completeness"] = completeness_score
    score += completeness_score

    # -----------------------------
    # 2. Emissions Coverage (30)
    # -----------------------------
    scope1_present = kpis["Scope 1 CO₂ (kg)"] > 0
    scope2_present = kpis["Scope 2 CO₂ (kg)"] > 0

    if scope1_present and scope2_present:
        emissions_score = 30
    elif scope1_present or scope2_present:
        emissions_score = 15
    else:
        emissions_score = 0

    breakdown["Emissions Coverage"] = emissions_score
    score += emissions_score

    # -----------------------------
    # 3. Renewable Transparency (20)
    # -----------------------------
    renewable_pct = kpis["Renewable Energy (%)"]

    if renewable_pct >= 40:
        renewable_score = 20
    elif renewable_pct >= 20:
        renewable_score = 12
    elif renewable_pct > 0:
        renewable_score = 6
    else:
        renewable_score = 0

    breakdown["Renewable Transparency"] = renewable_score
    score += renewable_score

    # -----------------------------
    # 4. Framework Alignment (20)
    # -----------------------------
    # Since CSRD + GRI mapping exists
    framework_score = 20
    breakdown["CSRD / GRI Alignment"] = framework_score
    score += framework_score

    return {
        "total_score": min(score, 100),
        "breakdown": breakdown,
    }
