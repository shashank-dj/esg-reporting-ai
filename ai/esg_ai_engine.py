def build_esg_context(kpis, audit, maturity, quality):
    return {
        "kpis": kpis,
        "audit_score": audit["total_score"],
        "audit_issues": audit["breakdown"],
        "maturity": maturity,
        "data_quality": quality
    }
