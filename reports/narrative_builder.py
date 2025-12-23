
"""
Narrative & Disclosure Builder
Generates human-readable ESG narrative text for reports and dashboards.
"""

def generate_esg_narrative(kpis, audit_score, maturity):
    """
    Generate ESG narrative sections based on KPIs, audit score, and CSRD maturity.

    Returns:
        dict: { "Environment": str, "Governance": str, "Strategy": str }
    """

    # -----------------------------
    # Environment Narrative
    # -----------------------------
    environment = (
        f"The organization reported total greenhouse gas emissions of "
        f"{kpis.get('Total CO₂ (kg)', 'N/A')} kg CO₂ during the reporting period. "
        f"Renewable energy contributed approximately "
        f"{kpis.get('Renewable Energy (%)', 'N/A')}% of total energy consumption. "
        "These figures reflect the organization’s current environmental footprint "
        "and progress toward decarbonization."
    )

    # -----------------------------
    # Governance Narrative
    # -----------------------------
    governance_strength = (
        "strong" if audit_score >= 80
        else "moderate" if audit_score >= 50
        else "developing"
    )

    governance = (
        f"The organization achieved an ESG audit readiness score of {audit_score}, "
        f"indicating {governance_strength} governance controls related to data quality, "
        "internal reporting processes, and regulatory preparedness. "
        "Ongoing improvements in data validation and documentation will further "
        "enhance audit confidence."
    )

    # -----------------------------
    # Strategy Narrative
    # -----------------------------
    strategy = (
        f"The organization is currently assessed at CSRD maturity level "
        f"{maturity.get('maturity_level', 'N/A')} "
        f"({maturity.get('maturity_label', 'N/A')}), "
        "indicating a structured approach to ESG integration and compliance. "
        "Future focus areas include expanding Scope 3 coverage, strengthening "
        "controls, and aligning ESG initiatives with long-term business strategy."
    )

    return {
        "Environment": environment,
        "Governance": governance,
        "Strategy": strategy,
    }
