from ai_analyzer import analyze_resume_with_ai, extract_skills_with_ai
from resume_parser import extract_text_from_pdf
from analyzer import (
    detect_sections,
    extract_skills,
    read_job_description,
    compare_skills,
    calculate_match_score,
    calculate_weighted_score,
    classify_job_skills,
    calculate_category_score,
    calculate_final_score,
    get_match_verdict,
    generate_recommendations,
    normalize_skill
)


resume_path = "resumes/sample_resume.pdf"
job_path = "jobs/job_description.txt"
resume_text = extract_text_from_pdf(resume_path)
job_text = read_job_description(job_path)

print("=== AI RESUME ANALYZER ===")
print()

sections = detect_sections(resume_text)

print("Sections detected:")

for section in sections:
    print(f"- {section}")
skills = extract_skills(resume_text)

print()
print("Skills detected:")

for skill in skills:
    print(f"- {skill}")
job_skills = extract_skills(job_text)

print()
print("Skills required by the job:")

for skill in job_skills:
    print(f"- {skill}")
matched_skills, missing_skills = compare_skills(skills, job_skills)

print()
print("Matched skills:")

for skill in matched_skills:
    print(f"- {skill}")

print()
print("Missing skills:")

for skill in missing_skills:
    print(f"- {skill}")

match_score = calculate_match_score(matched_skills, job_skills)

print()
print(f"Match score: {match_score}%")

weighted_score = calculate_weighted_score(skills, job_skills)
print()
print(f"Weighted match score: {weighted_score}%")
required_skills, preferred_skills, unclassified_skills = classify_job_skills(
    job_text,
    job_skills
)

print()
print("Required skills:")

for skill in required_skills:
    print(f"- {skill}")

print()
print("Preferred skills:")

for skill in preferred_skills:
    print(f"- {skill}")

print()
print("Unclassified skills:")

for skill in unclassified_skills:
    print(f"- {skill}")

required_score = calculate_category_score(
    skills,
    required_skills
)

preferred_score = calculate_category_score(
    skills,
    preferred_skills
)

print()
print(f"Required skills score: {required_score}%")

print()
print(f"Preferred skills score: {preferred_score}%")

final_score = calculate_final_score(
    required_score,
    preferred_score
)

print()
print(f"Final compatibility score: {final_score}%")

verdict = get_match_verdict(final_score)

print()
print(f"Match verdict: {verdict}")

recommendations = generate_recommendations(
    missing_skills,
    required_skills,
    preferred_skills
)

print()
print("Recommendations:")

for recommendation in recommendations:
    print(f"- {recommendation}")

print()
print("=== AI ANALYSIS ===")
print()

ai_analysis = analyze_resume_with_ai(
    resume_text,
    job_text
)

print(ai_analysis)

print()
print("=== AI SKILL EXTRACTION ===")
print()

ai_resume_skills = extract_skills_with_ai(resume_text)
ai_job_skills = extract_skills_with_ai(job_text)

print("AI-detected resume skills:")

for skill in ai_resume_skills:
    print(f"- {skill}")
print()
print("AI-detected job skills:")

for skill in ai_job_skills:
    print(f"- {skill}")


resume_skills_normalized = [
    normalize_skill(skill)
    for skill in ai_resume_skills
]
job_skills_normalized = [
    normalize_skill(skill)
    for skill in ai_job_skills
]

ai_matched_skills = []
ai_missing_skills = []

for skill in ai_job_skills:

    if normalize_skill(skill) in resume_skills_normalized:
        ai_matched_skills.append(skill)

    else:
        ai_missing_skills.append(skill)
print()
print("AI Matched Skills:")

for skill in ai_matched_skills:
    print(f"- {skill}")

print()
print("AI Missing Skills:")

for skill in ai_missing_skills:
    print(f"- {skill}")
if len(ai_job_skills) > 0:

    ai_match_score = (
        len(ai_matched_skills)
        / len(ai_job_skills)
    ) * 100

else:
    ai_match_score = 0

print()
print(f"AI Skill Match Score: {round(ai_match_score, 1)}%")