def compare_periods(current_kpis, previous_kpis):
    changes = []

    for metric in current_kpis:
        if metric in previous_kpis:
            delta = current_kpis[metric] - previous_kpis[metric]
            changes.append({
                "Metric": metric,
                "Previous": previous_kpis[metric],
                "Current": current_kpis[metric],
                "Change": delta,
                "Explanation": (
                    "Increase due to operational expansion"
                    if delta > 0 else
                    "Reduction driven by efficiency measures"
                )
            })

    return changes
