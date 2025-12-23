"""
AI Audit Risk Explainer
Explains audit readiness score drivers and remediation actions.
"""

def build_audit_risk_context(audit, data_quality, maturity):
    return {
        "audit_score": audit["total_score"],
        "audit_breakdown": audit["breakdown"],
        "data_quality_flags": data_quality["quality_flags"],
        "csrd_maturity": maturity
    }


def generate_ai_audit_explanation(context, llm_client):
    prompt = f"""
You are an ESG audit expert advising an organization.

Using ONLY the data below, explain:
1. Why the audit readiness score is at this level
2. Key risk drivers
3. Top 3 remediation actions to improve audit readiness

DATA:
{context}

RULES:
- Do not invent facts
- Base explanations strictly on provided data
- Be concise and professional
"""

    return llm_client.generate(prompt)
