import os

from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def analyze_resume_with_ai(resume_text, job_description):

    prompt = f"""
You are an AI resume analyst.

Analyze the candidate's resume against the provided job description.

Provide:

1. Overall Assessment
2. Main Strengths
3. Missing or Weak Skills
4. Resume Improvement Suggestions
5. Job-Specific Recommendations

Important rules:
- Only use information actually present in the resume.
- Do not invent experience, education, projects, or skills.
- Clearly distinguish between skills the candidate has and skills the job requires.
- Give practical recommendations for improving the resume.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text_parts = []
    for block in message.content:
        if block.type == "text":
            text_parts.append(block.text)
            return "\n".join(text_parts)