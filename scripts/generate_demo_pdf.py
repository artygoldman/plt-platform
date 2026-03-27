"""
Generate a fake blood test PDF for testing.

Creates a minimal but realistic blood test report PDF using reportlab.
"""

from pathlib import Path
from datetime import date, datetime
from io import BytesIO

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def create_pdf_with_reportlab(output_path: Path):
    """Create PDF using reportlab."""
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab not installed. Install with: pip install reportlab")

    # Create PDF
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        alignment=TA_CENTER,
    )
    story.append(Paragraph("LABORATORY TEST REPORT", title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Lab info
    lab_info = [
        ["Lab Name:", "Quest Diagnostics"],
        ["Report Date:", str(date.today())],
        ["Specimen Date:", str(date.today())],
        ["Patient Name:", "John Doe"],
        ["Patient ID:", "PID-12345"],
        ["Physician:", "Dr. Jane Smith"],
    ]

    lab_table = Table(lab_info, colWidths=[2*inch, 3*inch])
    lab_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f7')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    story.append(lab_table)
    story.append(Spacer(1, 0.3 * inch))

    # Test results
    results_title = ParagraphStyle(
        'ResultsTitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
    )
    story.append(Paragraph("COMPREHENSIVE METABOLIC PANEL", results_title))

    # Results table
    test_data = [
        ["Test Name", "Value", "Unit", "Reference Range", "Status"],
        ["Glucose", "95", "mg/dL", "70-100", "Normal"],
        ["Total Cholesterol", "195", "mg/dL", "<200", "Normal"],
        ["LDL Cholesterol", "110", "mg/dL", "<130", "Normal"],
        ["HDL Cholesterol", "55", "mg/dL", ">40", "Normal"],
        ["Triglycerides", "120", "mg/dL", "<150", "Normal"],
        ["ApoB", "1.1", "g/L", "<1.3", "Normal"],
        ["HbA1c", "5.2", "%", "<5.7", "Normal"],
        ["Creatinine", "0.9", "mg/dL", "0.7-1.3", "Normal"],
        ["AST", "28", "U/L", "10-34", "Normal"],
        ["ALT", "32", "U/L", "7-56", "Normal"],
    ]

    results_table = Table(test_data, colWidths=[2*inch, 1*inch, 0.8*inch, 1.5*inch, 0.8*inch])
    results_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    story.append(results_table)
    story.append(Spacer(1, 0.2 * inch))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER,
    )
    story.append(Paragraph(
        "This report is generated for testing purposes only. Not a real medical document.",
        footer_style
    ))

    # Build PDF
    doc.build(story)
    print(f"✓ PDF created: {output_path}")


def create_pdf_minimal(output_path: Path):
    """Create a minimal PDF without reportlab (fallback)."""
    # Create a minimal valid PDF structure
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources 4 0 R /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >>
endobj
5 0 obj
<< /Length 500 >>
stream
BT
/F1 12 Tf
50 750 Td
(LABORATORY TEST REPORT) Tj
0 -20 Td
(Lab: Quest Diagnostics) Tj
0 -15 Td
(Date: """ + str(date.today()).encode() + b""") Tj
0 -15 Td
(Patient: John Doe) Tj
0 -30 Td
(TEST RESULTS) Tj
0 -20 Td
(Glucose: 95 mg/dL - Normal) Tj
0 -15 Td
(Total Cholesterol: 195 mg/dL - Normal) Tj
0 -15 Td
(LDL: 110 mg/dL - Normal) Tj
0 -15 Td
(HDL: 55 mg/dL - Normal) Tj
0 -15 Td
(Triglycerides: 120 mg/dL - Normal) Tj
0 -15 Td
(HbA1c: 5.2% - Normal) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000214 00000 n
0000000313 00000 n
trailer
<< /Size 6 /Root 1 0 R >>
startxref
863
%%EOF
"""
    output_path.write_bytes(pdf_content)
    print(f"✓ Minimal PDF created: {output_path}")


def generate_demo_pdfs():
    """Generate demo blood test PDFs."""
    pdf_dir = Path("tests/fixtures")
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # Create multiple PDF versions for testing
    pdf_files = [
        "blood_test_sample.pdf",
        "blood_test_complete.pdf",
        "blood_test.pdf",
    ]

    for pdf_filename in pdf_files:
        output_path = pdf_dir / pdf_filename

        if output_path.exists():
            print(f"ℹ PDF already exists: {output_path}")
            continue

        try:
            if REPORTLAB_AVAILABLE:
                create_pdf_with_reportlab(output_path)
            else:
                create_pdf_minimal(output_path)
        except Exception as e:
            print(f"⚠ Error creating {pdf_filename}: {e}")
            # Fallback to minimal
            create_pdf_minimal(output_path)


def main():
    """Generate all demo PDFs."""
    print("Generating demo blood test PDFs...")
    generate_demo_pdfs()
    print("Done!")


if __name__ == "__main__":
    main()
