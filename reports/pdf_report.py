from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import io
from datetime import date


def generate_esg_pdf(kpis: dict) -> bytes:
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

    # -----------------------
    # Title
    # -----------------------
    elements.append(Paragraph("<b>ESG Environmental Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Report Date: {date.today()}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # -----------------------
    # Executive Summary
    # -----------------------
    summary = f"""
    This report summarizes the environmental performance of the organization.
    Total CO₂ emissions amount to <b>{kpis['Total CO₂ (kg)']} kg</b>, with
    renewable energy contributing <b>{kpis['Renewable Energy (%)']}%</b> of total
    electricity consumption.
    """

    elements.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(summary, styles["Normal"]))
    elements.append(Spacer(1, 20))

    # -----------------------
    # KPI Table
    # -----------------------
    table_data = [["Metric", "Value"]]
    for k, v in kpis.items():
        table_data.append([k, str(v)])

    table = Table(table_data, colWidths=[9 * cm, 5 * cm])
    elements.append(Paragraph("<b>Key ESG Metrics</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    return buffer.read()
