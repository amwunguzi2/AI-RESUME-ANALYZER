import streamlit as st
import tempfile

from resume_parser import extract_text_from_pdf
from analyzer import (
    extract_skills,
    compare_skills,
    classify_job_skills,
    calculate_category_score,
    calculate_final_score,
    get_match_verdict,
    generate_recommendations
)


st.title("AI Resume Analyzer")

st.write(
    "Upload your resume and paste a job description to analyze the match."
)

uploaded_resume = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the job description here",
    height=250
)

if st.button("Analyze"):

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

        st.header("Results")

        st.metric(
            "Compatibility Score",
            f"{final_score}%"
        )

        st.write(f"**Match verdict:** {verdict}")

        st.subheader("Matched Skills")

        if matched_skills:
            for skill in matched_skills:
                st.write(f"✅ {skill}")
        else:
            st.write("No matched skills detected.")

        st.subheader("Missing Skills")

        if missing_skills:
            for skill in missing_skills:
                st.write(f"❌ {skill}")
        else:
            st.write("No missing skills detected.")

        st.subheader("Required Skills Score")
        st.write(f"{required_score}%")

        st.subheader("Preferred Skills Score")
        st.write(f"{preferred_score}%")

        st.subheader("Recommendations")

        for recommendation in recommendations:
            st.write(f"- {recommendation}")