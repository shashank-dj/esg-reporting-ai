def get_esg_financial_linkage(kpis, audit_score, maturity_level):
    insights = []

    # Renewable energy impact
    renewable_pct = kpis["Renewable Energy (%)"]
    if renewable_pct < 25:
        energy_risk = "High"
    elif renewable_pct < 50:
        energy_risk = "Moderate"
    else:
        energy_risk = "Low"

    insights.append({
        "ESG Driver": "Renewable Energy Usage",
        "Financial Area": "Energy Cost Volatility",
        "Impact Type": "Cost Risk Reduction",
        "Current Status": f"{renewable_pct}%",
        "Financial Signal": energy_risk,
        "Explanation": "Higher renewable share reduces exposure to energy price volatility"
    })

    # Emissions impact
    insights.append({
        "ESG Driver": "Scope 1 & 2 Emissions",
        "Financial Area": "Carbon Cost Exposure",
        "Impact Type": "Regulatory Risk",
        "Current Status": f"{kpis['Total CO₂ (kg)']} kg",
        "Financial Signal": "Moderate",
        "Explanation": "Lower emissions reduce future carbon pricing and compliance costs"
    })

    # Audit readiness impact
    audit_risk = "Low" if audit_score >= 80 else "Moderate" if audit_score >= 50 else "High"

    insights.append({
        "ESG Driver": "Audit Readiness",
        "Financial Area": "Compliance & Penalty Risk",
        "Impact Type": "Risk Mitigation",
        "Current Status": f"Score {audit_score}",
        "Financial Signal": audit_risk,
        "Explanation": "Higher readiness lowers probability of penalties and audit overruns"
    })

    # Maturity impact
    insights.append({
        "ESG Driver": "CSRD Maturity",
        "Financial Area": "Long-term Value & Cost of Capital",
        "Impact Type": "Strategic Value",
        "Current Status": f"Level {maturity_level}",
        "Financial Signal": "Improving" if maturity_level >= 3 else "Weak",
        "Explanation": "Higher ESG maturity improves investor confidence and financing access"
    })

    return insights
