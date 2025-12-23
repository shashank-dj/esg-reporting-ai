"""
AI-powered ESG Narrative Copilot
Grounded, audit-safe narrative generation
"""

def build_esg_context(kpis, audit, maturity, data_quality):
    return {
        "kpis": kpis,
        "audit_score": audit["total_score"],
        "audit_breakdown": audit["breakdown"],
        "maturity": maturity,
        "data_quality": data_quality["quality_flags"]
    }


def generate_ai_narrative(context, llm_client):
    """
    Uses an LLM client to generate ESG narrative.
    The model is strictly grounded in provided context.
    """

    prompt = f"""
You are a senior ESG reporting consultant.

Generate a professional ESG narrative using ONLY the data provided.
Do not assume or invent any facts.

DATA:
{context}

STRUCTURE:
1. Environment
2. Governance
3. Strategy

STYLE:
- Formal
- Audit-ready
- Plain English
- No marketing language
"""

    response = llm_client.generate(prompt)
    return response
