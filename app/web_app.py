import streamlit as st
import tempfile
from io import BytesIO
import re
from datetime import datetime

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

from resume_parser import extract_text_from_pdf
from ai_analyzer import analyze_resume_with_ai, extract_skills_with_ai

from analyzer import (
    extract_skills,
    compare_skills,
    classify_job_skills,
    calculate_category_score,
    calculate_final_score,
    get_match_verdict,
    generate_recommendations,
    normalize_skill
)
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    Table,
    TableStyle,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle

def convert_markdown_bold(text):
    return re.sub(
        r"\*\*(.+?)\*\*",
        r"<b>\1</b>",
        text
    )

def add_page_number(canvas, doc):

    canvas.saveState()

    page_number = canvas.getPageNumber()

    footer_text = f"AI Resume Analyzer  |  Page {page_number}"

    canvas.setFont("Helvetica", 8)

    canvas.drawCentredString(
        letter[0] / 2,
        25,
        footer_text
    )

    canvas.restoreState()

def create_pdf_report(
    ai_match_score,
    ai_matched_skills,
    ai_missing_skills,
    ai_analysis,
    job_title="Analyzed Position"
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=8
    )
    score_style = ParagraphStyle(
        "ScoreStyle",
        parent=styles["Heading1"],
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=16
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        spaceAfter=6
    )
    header_subtitle_style = ParagraphStyle(
        "HeaderSubtitle",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        alignment=TA_CENTER,
        spaceAfter=4
    )

    verdict_style = ParagraphStyle(
        "VerdictStyle",
        parent=styles["BodyText"],
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=4
    )
    analysis_title_style = ParagraphStyle(
        "AnalysisTitle",
        parent=styles["Heading1"],
        fontSize=16,
        leading=20,
        spaceBefore=8,
        spaceAfter=12
    )

    story = []
    
    if ai_match_score >= 70:
        score_message = "Strong match"
    elif ai_match_score >= 40:
        score_message = "Moderate match"
    else:
        score_message = "Low match"
    header_data = [
        [
            Paragraph(
                "AI RESUME ANALYZER",
                title_style
            )
        ],
        [
            Paragraph(
                "ANALYSIS REPORT",
                header_subtitle_style
            )
        ],
        [
            Paragraph(
                f"{round(ai_match_score, 1)}%",
                score_style
            )
        ],
        [
            Paragraph(
                score_message.upper(),
                verdict_style
            )
        ]
    ]
    header_table = Table(
        header_data,
        colWidths=[500]
    )
    header_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F8")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#D0D5DD")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])
    )
    story.append(header_table)
    story.append(Spacer(1, 24))
    generated_date = datetime.now().strftime("%B %d, %Y")
    meta_table = Table(
        [  
            [
                Paragraph(
                    f"<b>Position:</b> {job_title}",
                    body_style
                ),
                Paragraph(
                    f"<b>Generated:</b> {generated_date}",
                    body_style
                )
            ]
        ],
        colWidths=[245, 245]
    )

    meta_table.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(meta_table)
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "Match Overview",
            section_style
        )
    )
    
    story.append(Spacer(1, 10))

    matched_content = [
        Paragraph(
            "<b>Matched Skills</b>",
            section_style
        )
    ]
    
    if ai_matched_skills:
        for skill in ai_matched_skills:
            matched_content.append(
                Paragraph(
                    f"• {skill}",
                    body_style
                )
            )
    else:
        matched_content.append(
            Paragraph(
                "No matched skills detected.",
                body_style
            )
        )
    
    missing_content = [
        Paragraph(
            "<b>Missing Skills</b>",
            section_style
        )
    ]
    
    if ai_missing_skills:
        for skill in ai_missing_skills:
            missing_content.append(
                Paragraph(
                    f"• {skill}",
                    body_style
                )
            )
    else:
        missing_content.append(
            Paragraph(
                "No missing skills detected.",
                body_style
            )
        )


    skills_table = Table(
        [
            [
                matched_content,
                missing_content
            ]
        ],
        colWidths=[245, 245]
    )

    skills_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#F7FAFC")),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#FFF7F7")),
            ("BOX", (0, 0), (0, 0), 1, colors.HexColor("#D9E2EC")),
            ("BOX", (1, 0), (1, 0), 1, colors.HexColor("#F0D3D3")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ])
    )

    story.append(skills_table)

    story.append(Spacer(1, 20))


    story.append(
        Paragraph(
            "Detailed AI Analysis",
            section_style
        )
    )

    lines = ai_analysis.split("\n")
    i = 0

    while i < len(lines):

        paragraph = lines[i].strip()

        if not paragraph:
            i += 1
            continue

        # Markdown table detection
        if paragraph.startswith("|") and paragraph.endswith("|"):

            table_rows = []

            while (
                i < len(lines)
                and lines[i].strip().startswith("|")
                and lines[i].strip().endswith("|")
            ):
                row = lines[i].strip()

                cells = [
                    cell.strip()
                    for cell in row.strip("|").split("|")
                ]

                table_rows.append(cells)
                i += 1

            # Remove separator row like |---|---|
            cleaned_rows = []

            for row in table_rows:
                if all(
                    re.fullmatch(r":?-{3,}:?", cell)
                    for cell in row
                ):
                    continue

                cleaned_rows.append(row)

            if cleaned_rows:

                pdf_table_data = []

                for row_index, row in enumerate(cleaned_rows):

                    pdf_row = []

                    for cell in row:
                        cell = convert_markdown_bold(cell)

                        style_to_use = (
                            header_subtitle_style
                            if row_index == 0
                            else body_style
                        )

                        pdf_row.append(
                            Paragraph(
                                cell,
                                style_to_use
                            )
                        )

                    pdf_table_data.append(pdf_row)

                column_count = len(pdf_table_data[0])
                table_width = 490
                column_width = table_width / column_count

                markdown_table = Table(
                    pdf_table_data,
                    colWidths=[column_width] * column_count
                )

                markdown_table.setStyle(
                    TableStyle([
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F2F4F7")),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D5DD")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ])
                )

                story.append(markdown_table)
                story.append(Spacer(1, 12))

            continue

        if paragraph.startswith("## "):
            clean_text = paragraph.replace("## ", "", 1)

            story.append(
                Paragraph(
                    clean_text,
                    section_style
                )
            )

            story.append(Spacer(1, 6))

        elif paragraph.startswith("# "):
            clean_text = paragraph.replace("# ", "", 1)
            clean_text = convert_markdown_bold(clean_text)

            story.append(
                Paragraph(
                    clean_text,
                    analysis_title_style
                )
            )

            story.append(Spacer(1, 8))

        elif paragraph.startswith("- "):
            clean_text = paragraph[2:]
            clean_text = convert_markdown_bold(clean_text)

            story.append(
                Paragraph(
                    f"• {clean_text}",
                    body_style
                )
            )

            story.append(Spacer(1, 4))

        else:
            clean_text = convert_markdown_bold(paragraph)

            story.append(
                Paragraph(
                    clean_text,
                    body_style
                )
            )

            story.append(Spacer(1, 6))

        i += 1

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )
    buffer.seek(0)

    return buffer.getvalue()

st.title("📄 AI Resume Analyzer")

st.markdown(
    """
    Compare your resume with a job description, identify matching and missing skills,
    calculate compatibility scores, and generate AI-powered recommendations.
    """
)

st.divider()
input_col1, input_col2 = st.columns(2)
with input_col1:
    st.subheader("1. Upload Resume")
    uploaded_resume = st.file_uploader(
        "Upload your resume",
        type=["pdf"]
    )


with input_col2:
    st.subheader("2. Job Description")
    job_title = st.text_input(
        "Job title",
        placeholder="e.g. Software Engineering Intern"
    )
    job_description = st.text_area(
        "Paste the job description here",
        height=250
    )

st.write("")

if st.button(
    "Analyze Resume",
    type="primary",
    use_container_width=True
):
    
    if uploaded_resume is None:
        st.warning("Please upload a resume.")

    elif not job_description.strip():
        st.warning("Please paste a job description.")

    else:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(uploaded_resume.read())
            temp_resume_path = temp_file.name

        resume_text = extract_text_from_pdf(temp_resume_path)
        st.session_state["resume_text"] = resume_text
        st.session_state["job_description"] = job_description
        st.session_state["job_title"] = (
            job_title.strip()
            if job_title.strip()
            else "Analyzed Position"
        )
        for key in [
            "ai_analysis",
            "ai_resume_skills",
            "ai_job_skills",
            "ai_matched_skills",
            "ai_missing_skills",
            "ai_match_score"
        ]:
            st.session_state.pop(key, None)

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        matched_skills, missing_skills = compare_skills(
            resume_skills,
            job_skills
        )

        required_skills, preferred_skills, unclassified_skills = (
            classify_job_skills(
                job_description,
                job_skills
            )
        )

        required_score = calculate_category_score(
            resume_skills,
            required_skills
        )

        preferred_score = calculate_category_score(
            resume_skills,
            preferred_skills
        )

        final_score = calculate_final_score(
            required_score,
            preferred_score
        )

        verdict = get_match_verdict(final_score)

        recommendations = generate_recommendations(
            missing_skills,
            required_skills,
            preferred_skills
        )

        st.header("Analysis Results")

        score_col, required_col, preferred_col = st.columns(3)

        with score_col:
            st.metric(
                "Overall Compatibility",
                f"{final_score}%"
            )

        with required_col:
            st.metric(
                "Required Skills Match",
                f"{required_score}%"
            )

        with preferred_col:
            st.metric(
                "Preferred Skills Match",
                f"{preferred_score}%"
            )

        st.progress(min(int(final_score), 100))

        if final_score >= 70:
            st.success(f"Match Verdict: {verdict}")
        elif final_score >= 40:
            st.warning(f"Match Verdict: {verdict}")
        else:
            st.error(f"Match Verdict: {verdict}")

        st.divider()

        matched_col, missing_col = st.columns(2)

        with matched_col:
            st.subheader("✅ Matched Skills")

            if matched_skills:
                for skill in matched_skills:
                    st.write(f"- {skill.title()}")
            else:
                st.write("No matched skills detected.")

        with missing_col:
            st.subheader("❌ Missing Skills")

            if missing_skills:
                for skill in missing_skills:
                    st.write(f"- {skill.title()}")
            else:
                st.write("No missing skills detected.")

        st.divider()

        st.subheader("💡 Recommendations")

        for recommendation in recommendations:
            st.write(f"- {recommendation}")

if (
    "resume_text" in st.session_state
    and "job_description" in st.session_state
):

    st.divider()

    st.header("AI-Powered Analysis")

    st.write(
        "Get a deeper analysis of your resume using Claude AI."
    )

    if st.button(
        "✨ Generate AI Analysis",
        use_container_width=True
    ):

        with st.spinner("Claude is analyzing your resume..."):
            ai_analysis = analyze_resume_with_ai(
                st.session_state["resume_text"],
                st.session_state["job_description"]
            )
            ai_resume_skills = extract_skills_with_ai(
                st.session_state["resume_text"]
            )
            ai_job_skills = extract_skills_with_ai(
                st.session_state["job_description"]
            )
            resume_skills_normalized = [
                normalize_skill(skill)
                for skill in ai_resume_skills
            ]
            ai_matched_skills = []
            ai_missing_skills = []
            
            for skill in ai_job_skills:
                if normalize_skill(skill) in resume_skills_normalized:
                    ai_matched_skills.append(skill)
                else:
                    ai_missing_skills.append(skill)
            
            if len(ai_job_skills) > 0:
                ai_match_score = (
                    len(ai_matched_skills)
                    / len(ai_job_skills)
                ) * 100
            else:
                ai_match_score = 0
            st.session_state["ai_analysis"] = ai_analysis
            st.session_state["ai_resume_skills"] = ai_resume_skills
            st.session_state["ai_job_skills"] = ai_job_skills
            st.session_state["ai_matched_skills"] = ai_matched_skills
            st.session_state["ai_missing_skills"] = ai_missing_skills
            st.session_state["ai_match_score"] = ai_match_score


if "ai_analysis" in st.session_state:

    ai_analysis = st.session_state["ai_analysis"]
    ai_resume_skills = st.session_state["ai_resume_skills"]
    ai_job_skills = st.session_state["ai_job_skills"]
    ai_matched_skills = st.session_state["ai_matched_skills"]
    ai_missing_skills = st.session_state["ai_missing_skills"]
    ai_match_score = st.session_state["ai_match_score"]

    st.subheader("🤖 Detailed AI Resume Analysis")

    with st.container(border=True):
        st.markdown(ai_analysis)

    st.divider()

    st.subheader("✨ AI Skills Analysis")

    ai_score = round(ai_match_score, 1)

    st.metric(
        "AI Skill Match Score",
        f"{ai_score}%"
    )

    st.progress(
        min(int(ai_match_score), 100)
    )

    if ai_match_score >= 70:
        st.success("Strong AI-detected skill match")

    elif ai_match_score >= 40:
        st.warning("Moderate AI-detected skill match")

    else:
        st.error("Low AI-detected skill match")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### ✅ Matched Skills")

        for skill in ai_matched_skills:
            st.write(f"- {skill}")

    with col2:
        st.write("### ❌ Missing Skills")

        for skill in ai_missing_skills:
            st.write(f"- {skill}")

    with st.expander("📄 View all skills detected in the resume"):
        for skill in ai_resume_skills:
            st.write(f"- {skill}")

    with st.expander("💼 View all skills detected in the job description"):
        for skill in ai_job_skills:
            st.write(f"- {skill}")

    report_text = f"""
AI RESUME ANALYZER REPORT

AI Skill Match Score: {round(ai_match_score, 1)}%

MATCHED SKILLS
{chr(10).join("- " + skill for skill in ai_matched_skills)}

MISSING SKILLS
{chr(10).join("- " + skill for skill in ai_missing_skills)}

DETAILED AI ANALYSIS

{ai_analysis}
"""

    st.divider()
    st.subheader("📥 Download Report")
    st.download_button(
        label="Download Analysis Report",
        data=report_text,
        file_name="ai_resume_analysis_report.txt",
        mime="text/plain",
        use_container_width=True
    )
    pdf_report = create_pdf_report(
        ai_match_score,
        ai_matched_skills,
        ai_missing_skills,
        ai_analysis,
        job_title=st.session_state.get(
            "job_title",
            "Analyzed Position"
        )
    )
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_report,
        file_name="ai_resume_analysis_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )