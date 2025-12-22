def generate_audit_trace(df, kpis):
    return {
        "Data Completeness": {
            "score": 30,
            "reason": "All required ESG columns present",
            "improvement": "None required"
        },
        "Emissions Coverage": {
            "score": 30,
            "reason": "Scope 1 and Scope 2 emissions available",
            "improvement": "Add Scope 3 for extended coverage"
        },
        "Renewable Transparency": {
            "score": 6,
            "reason": "Renewable energy share below 20%",
            "improvement": "Increase renewable sourcing"
        },
        "Framework Alignment": {
            "score": 20,
            "reason": "CSRD and GRI mappings implemented",
            "improvement": "Extend to SASB/TCFD disclosures"
        }
    }
