def get_framework_coverage():
    """
    Framework coverage matrix for ESG topics.
    Coverage legend:
    ✔ = Compliant
    ⚠ = Partial
    ❌ = Not Covered
    """

    return [
        {
            "ESG Topic": "Energy Consumption",
            "CSRD": "✔",
            "GRI": "✔",
            "SASB": "✔",
            "TCFD": "⚠",
        },
        {
            "ESG Topic": "Scope 1 Emissions",
            "CSRD": "✔",
            "GRI": "✔",
            "SASB": "✔",
            "TCFD": "✔",
        },
        {
            "ESG Topic": "Scope 2 Emissions",
            "CSRD": "✔",
            "GRI": "✔",
            "SASB": "✔",
            "TCFD": "✔",
        },
        {
            "ESG Topic": "Scope 3 Emissions",
            "CSRD": "⚠",
            "GRI": "⚠",
            "SASB": "⚠",
            "TCFD": "❌",
        },
        {
            "ESG Topic": "Climate Risk Management",
            "CSRD": "⚠",
            "GRI": "❌",
            "SASB": "❌",
            "TCFD": "⚠",
        },
        {
            "ESG Topic": "Targets & Transition Plan",
            "CSRD": "❌",
            "GRI": "❌",
            "SASB": "❌",
            "TCFD": "⚠",
        },
    ]
