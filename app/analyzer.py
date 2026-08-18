import re

def detect_sections(resume_text):

    section_names = {
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "professional profile",
        "career summary"
    ],
    "education": [
        "education",
        "academic background"
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience"
    ],
    "skills": [
        "skills",
        "technical skills",
        "core competencies"
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects"
    ],
    "certifications": [
        "certifications",
        "certificates"
    ],
    "volunteer work": [
        "volunteer work",
        "volunteering",
        "volunteer experience",
        "community involvement",
        "community service"
    ]
}

    detected_sections = []

    text_lower = resume_text.lower()

    for section, possible_names in section_names.items():

        for name in possible_names:

            if name in text_lower:
                detected_sections.append(section)
                break

    return detected_sections
def extract_skills(resume_text):

    known_skills = [
        "python",
        "java",
        "javascript",
        "typescript",
        "sql",
        "html",
        "css",
        "react",
        "node.js",
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "linux",
        "c",
        "c++",
        "c#",
        "matlab",
        "excel",
        "power bi"
    ]

    detected_skills = []

    text_lower = resume_text.lower()

    for skill in known_skills:
        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
        if re.search(pattern, text_lower):
            detected_skills.append(skill)

    return detected_skills
def read_job_description(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        job_text = file.read()

    return job_text
def compare_skills(resume_skills, job_skills):

    matched_skills = []
    missing_skills = []

    for skill in job_skills:

        if skill in resume_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    return matched_skills, missing_skills
def calculate_match_score(matched_skills, job_skills):

    if len(job_skills) == 0:
        return 0

    score = (len(matched_skills) / len(job_skills)) * 100

    return round(score, 1)
def calculate_weighted_score(resume_skills, job_skills):

    skill_weights = {
        "python": 3,
        "java": 3,
        "javascript": 3,
        "typescript": 3,
        "sql": 3,
        "react": 2,
        "node.js": 2,
        "git": 2,
        "github": 1,
        "docker": 2,
        "aws": 3,
        "azure": 3,
        "linux": 2,
        "c": 3,
        "c++": 3,
        "c#": 3,
        "matlab": 2,
        "excel": 1,
        "power bi": 2
    }

    total_weight = 0
    matched_weight = 0

    for skill in job_skills:

        weight = skill_weights.get(skill, 1)

        total_weight += weight

        if skill in resume_skills:
            matched_weight += weight

    if total_weight == 0:
        return 0

    score = (matched_weight / total_weight) * 100

    return round(score, 1)
def classify_job_skills(job_text, job_skills):

    required_keywords = [
        "required",
        "must have",
        "must-have",
        "essential",
        "mandatory",
        "should have",
        "need to have",
        "needs to have"
    ]

    preferred_keywords = [
        "preferred",
        "nice to have",
        "nice-to-have",
        "asset",
        "considered an asset"
    ]

    required_skills = []
    preferred_skills = []
    unclassified_skills = []

    job_text_lower = job_text.lower()

    sentences = re.split(r'[.!?\n]+', job_text_lower)

    for skill in job_skills:

        classified = False

        for sentence in sentences:

            pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'

            if re.search(pattern, sentence):

                # On vérifie "preferred" en premier
                if any(keyword in sentence for keyword in preferred_keywords):
                    preferred_skills.append(skill)
                    classified = True
                    break

                elif any(keyword in sentence for keyword in required_keywords):
                    required_skills.append(skill)
                    classified = True
                    break

        if not classified:
            unclassified_skills.append(skill)

    return required_skills, preferred_skills, unclassified_skills

def calculate_category_score(resume_skills, target_skills):

    if len(target_skills) == 0:
        return 0

    matched = 0

    for skill in target_skills:
        if skill in resume_skills:
            matched += 1

    score = (matched / len(target_skills)) * 100

    return round(score, 1)

def calculate_final_score(required_score, preferred_score):

    final_score = (
        required_score * 0.8
        + preferred_score * 0.2
    )

    return round(final_score, 1)

def get_match_verdict(final_score):

    if final_score >= 80:
        return "Excellent match"

    elif final_score >= 60:
        return "Strong match"

    elif final_score >= 40:
        return "Moderate match"

    else:
        return "Low match"
    
def generate_recommendations(missing_skills, required_skills, preferred_skills):

    recommendations = []

    missing_required = []

    for skill in missing_skills:
        if skill in required_skills:
            missing_required.append(skill)

    missing_preferred = []

    for skill in missing_skills:
        if skill in preferred_skills:
            missing_preferred.append(skill)

    if missing_required:
        recommendations.append(
            "Focus on required skills: " + ", ".join(missing_required)
        )

    if missing_preferred:
        recommendations.append(
            "Consider adding preferred skills: " + ", ".join(missing_preferred)
        )

    if not recommendations:
        recommendations.append(
            "Your resume covers all identified job skills."
        )

    return recommendations