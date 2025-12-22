def get_sasb_mapping():
    """
    Initial SASB-aligned mapping for climate & energy metrics.
    Industry-agnostic baseline (acceptable for early-stage ESG tools).
    """
    return [
        {
            "metric": "Energy Consumption",
            "sasb": "IF-EU-130a.1 – Energy Management",
        },
        {
            "metric": "Scope 1 GHG Emissions",
            "sasb": "IF-EU-110a.1 – Gross global Scope 1 emissions",
        },
        {
            "metric": "Scope 2 GHG Emissions",
            "sasb": "IF-EU-110a.1 – Gross global Scope 2 emissions",
        },
        {
            "metric": "Renewable Energy Use",
            "sasb": "IF-EU-130a.2 – Renewable energy usage",
        },
    ]
