def get_csrd_gri_mapping():
    """
    Maps ESG metrics to CSRD (ESRS) and GRI standards
    """
    return [
        {
            "metric": "Total Energy Consumption",
            "csrd": "ESRS E1 – Climate Change (Energy)",
            "gri": "GRI 302-1 – Energy consumption within the organization",
        },
        {
            "metric": "Renewable Energy Percentage",
            "csrd": "ESRS E1 – Climate Change (Renewables)",
            "gri": "GRI 302-1 / 302-4 – Reduction of energy consumption",
        },
        {
            "metric": "Scope 1 CO₂ Emissions",
            "csrd": "ESRS E1 – Scope 1 GHG emissions",
            "gri": "GRI 305-1 – Direct (Scope 1) GHG emissions",
        },
        {
            "metric": "Scope 2 CO₂ Emissions",
            "csrd": "ESRS E1 – Scope 2 GHG emissions",
            "gri": "GRI 305-2 – Energy indirect (Scope 2) GHG emissions",
        },
        {
            "metric": "Total CO₂ Emissions",
            "csrd": "ESRS E1 – Total GHG emissions",
            "gri": "GRI 305-1 / 305-2",
        },
    ]
