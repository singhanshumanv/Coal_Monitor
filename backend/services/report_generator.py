from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(project_name, tasks):

    file_path = "compliance_report.pdf"

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Mining Compliance Report", styles['Title']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Project: {project_name}", styles['Normal']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Compliance Tasks:", styles['Heading2']))
    elements.append(Spacer(1, 10))

    for task in tasks:
        text = f"{task['compliance_type']} - Deadline: {task['deadline']} - Status: {task['status']}"
        elements.append(Paragraph(text, styles['Normal']))
        elements.append(Spacer(1, 5))

    doc = SimpleDocTemplate(file_path)
    doc.build(elements)

    return file_path