def get_tcfd_mapping():
    """
    TCFD-aligned disclosure mapping focused on Metrics & Targets
    and Risk Management (climate-related).
    """
    return [
        {
            "area": "Metrics & Targets",
            "tcfd": "Disclose Scope 1 and Scope 2 GHG emissions",
            "coverage": "Implemented",
        },
        {
            "area": "Metrics & Targets",
            "tcfd": "Describe targets used to manage climate risks",
            "coverage": "Partial",
        },
        {
            "area": "Risk Management",
            "tcfd": "Describe how climate risks are identified",
            "coverage": "Not Implemented",
        },
    ]
