from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import io
from datetime import date


def generate_csrd_gap_pdf(kpis: dict, audit_score: int) -> bytes:
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    elements = []

    # -----------------------------
    # Title
    # -----------------------------
    elements.append(Paragraph("<b>CSRD Gap Analysis Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Report Date: {date.today()}", styles["Normal"]))
    elements.append(Paragraph(f"Audit Readiness Score: <b>{audit_score}/100</b>", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # -----------------------------
    # Summary
    # -----------------------------
    summary = """
    This report evaluates the organization’s readiness against the
    Corporate Sustainability Reporting Directive (CSRD), focusing on
    ESRS E1 – Climate Change disclosures.
    """

    elements.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(summary, styles["Normal"]))
    elements.append(Spacer(1, 20))

    # -----------------------------
    # Gap Table
    # -----------------------------
    table_data = [
        ["CSRD Requirement (ESRS E1)", "Status", "Gap / Recommendation"],
        [
            "Energy Consumption Disclosure",
            "✔ Compliant" if kpis["Total Energy (kWh)"] > 0 else "❌ Missing",
            "Ensure continuous energy data capture across facilities.",
        ],
        [
            "Scope 1 GHG Emissions",
            "✔ Compliant" if kpis["Scope 1 CO₂ (kg)"] > 0 else "❌ Missing",
            "Fuel consumption data must be tracked consistently.",
        ],
        [
            "Scope 2 GHG Emissions",
            "✔ Compliant" if kpis["Scope 2 CO₂ (kg)"] > 0 else "❌ Missing",
            "Grid electricity emissions should be calculated using regional factors.",
        ],
        [
            "Renewable Energy Share",
            "⚠ Partial" if kpis["Renewable Energy (%)"] < 40 else "✔ Compliant",
            "Increase renewable sourcing or improve traceability.",
        ],
    ]

    table = Table(table_data, colWidths=[6 * cm, 3 * cm, 6 * cm])
    elements.append(Paragraph("<b>CSRD Gap Analysis</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))
    elements.append(table)

    # -----------------------------
    # Recommendations
    # -----------------------------
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<b>Key Recommendations</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    recommendations = """
    • Improve renewable energy procurement transparency.<br/>
    • Expand emissions accounting to Scope 3 categories.<br/>
    • Automate ESG data validation to improve audit readiness.
    """

    elements.append(Paragraph(recommendations, styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer.read()
