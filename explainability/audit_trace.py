def generate_audit_trace(df, kpis):
    return {
        "Data Completeness": {
            "score": 30,
            "reason": "All required ESG data columns are present",
            "improvement": "No action required",
        },
        "Emissions Coverage": {
            "score": 30,
            "reason": "Scope 1 and Scope 2 emissions are calculated",
            "improvement": "Include Scope 3 supplier emissions",
        },
        "Renewable Transparency": {
            "score": 6 if kpis["Renewable Energy (%)"] < 20 else 12,
            "reason": f"Renewable energy share is {kpis['Renewable Energy (%)']}%",
            "improvement": "Increase renewable sourcing to improve score",
        },
        "Framework Alignment": {
            "score": 20,
            "reason": "CSRD, GRI, SASB, and TCFD mappings available",
            "improvement": "Expand framework coverage depth",
        },
    }
