import pandas as pd

# Emission factors (simplified, realistic)
GRID_EMISSION_FACTOR = 0.82   # kg CO2 per kWh
FUEL_EMISSION_FACTOR = 2.31   # kg CO2 per liter (diesel)

def calculate_emissions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["scope_2_co2_kg"] = (df["energy_kwh"] - df["renewable_kwh"]) * GRID_EMISSION_FACTOR
    df["scope_1_co2_kg"] = df["fuel_liters"] * FUEL_EMISSION_FACTOR
    df["total_co2_kg"] = df["scope_1_co2_kg"] + df["scope_2_co2_kg"]

    return df


def aggregate_kpis(df: pd.DataFrame) -> dict:
    return {
        "Total Energy (kWh)": int(df["energy_kwh"].sum()),
        "Renewable Energy (%)": round(
            (df["renewable_kwh"].sum() / df["energy_kwh"].sum()) * 100, 2
        ),
        "Scope 1 CO₂ (kg)": round(df["scope_1_co2_kg"].sum(), 2),
        "Scope 2 CO₂ (kg)": round(df["scope_2_co2_kg"].sum(), 2),
        "Total CO₂ (kg)": round(df["total_co2_kg"].sum(), 2),
    }
