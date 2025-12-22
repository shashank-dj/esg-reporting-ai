import pandas as pd

# Simplified spend-based emission factors (kg CO2 / €)
EMISSION_FACTORS = {
    "raw_materials": 0.45,
    "logistics": 0.18,
    "it_services": 0.05,
    "manufacturing_services": 0.32,
}


def estimate_scope3_emissions(spend_data: pd.DataFrame) -> pd.DataFrame:
    """
    Expected columns:
    - category
    - annual_spend_eur
    """
    df = spend_data.copy()

    df["emission_factor"] = df["category"].map(EMISSION_FACTORS)
    df["scope3_co2_kg"] = df["annual_spend_eur"] * df["emission_factor"]

    return df


def aggregate_scope3_kpi(df: pd.DataFrame) -> float:
    return round(df["scope3_co2_kg"].sum(), 2)
