from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os
import re
from datetime import datetime

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "text")

def create_pdf(summary: str, quiz: list) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "summary_quiz.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold"
    )

    subtitle_style = ParagraphStyle(
        "SubTitle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#6b7280"),
        spaceAfter=20,
        alignment=TA_CENTER
    )

    section_header_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading1"],
        fontSize=15,
        textColor=colors.HexColor("#1a1a2e"),
        spaceBefore=18,
        spaceAfter=10,
        fontName="Helvetica-Bold",
        borderPad=4
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#374151"),
        leading=16,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#1f2937"),
        fontName="Helvetica-Bold",
        spaceBefore=10,
        spaceAfter=4
    )

    question_style = ParagraphStyle(
        "Question",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#1f2937"),
        fontName="Helvetica-Bold",
        spaceBefore=12,
        spaceAfter=4
    )

    option_style = ParagraphStyle(
        "Option",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#4b5563"),
        leftIndent=20,
        spaceAfter=2
    )

    answer_style = ParagraphStyle(
        "Answer",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#059669"),
        leftIndent=20,
        fontName="Helvetica-Bold",
        spaceAfter=2
    )

    explanation_style = ParagraphStyle(
        "Explanation",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#6b7280"),
        leftIndent=20,
        spaceAfter=4,
        fontName="Helvetica-Oblique"
    )

    story = []

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("AI Video Summarizer", title_style))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a1a2e")))
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph("Video Summary", section_header_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#d1d5db")))
    story.append(Spacer(1, 0.1 * inch))

    for line in summary.split("\n"):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 4))
            continue
        if line.startswith("### "):
            story.append(Paragraph(line[4:], heading_style))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], heading_style))
        elif line.startswith("# "):
            story.append(Paragraph(line[2:], heading_style))
        elif line.startswith("**") and line.endswith("**"):
            story.append(Paragraph(line[2:-2], heading_style))
        elif line.startswith("- ") or line.startswith("* "):
            clean = line[2:]
            clean = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", clean)
            story.append(Paragraph(f"- {clean}", body_style))
        else:
            clean = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            story.append(Paragraph(clean, body_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a1a2e")))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Comprehension Quiz", section_header_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#d1d5db")))
    story.append(Spacer(1, 0.1 * inch))

    for i, item in enumerate(quiz):
        question = item.get("question", "")
        options = item.get("options", {})
        answer = item.get("answer", "")
        explanation = item.get("explanation", "")

        story.append(Paragraph(f"Q{i + 1}. {question}", question_style))

        for key in ["A", "B", "C", "D"]:
            opt_text = options.get(key, "")
            if key == answer:
                story.append(Paragraph(f"  {key}. {opt_text} (Correct)", answer_style))
            else:
                story.append(Paragraph(f"  {key}. {opt_text}", option_style))

        if explanation:
            story.append(Paragraph(f"Explanation: {explanation}", explanation_style))

        story.append(Spacer(1, 0.05 * inch))

    story.append(Spacer(1, 0.3 * inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#d1d5db")))
    story.append(Paragraph("Generated by AI Video Summarizer - Powered by Whisper + Groq", subtitle_style))

    doc.build(story)
    return pdf_path