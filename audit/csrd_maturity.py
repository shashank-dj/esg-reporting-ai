def calculate_csrd_maturity(year: int, audit_score: int, scope3_present: bool) -> dict:
    if audit_score >= 85 and scope3_present:
        level = 5
        label = "Optimized"
    elif audit_score >= 70:
        level = 4
        label = "Managed"
    elif audit_score >= 50:
        level = 3
        label = "Defined"
    elif audit_score >= 30:
        level = 2
        label = "Basic"
    else:
        level = 1
        label = "Ad-hoc"

    return {
        "year": year,
        "maturity_level": level,
        "maturity_label": label,
        "audit_score": audit_score,
    }
