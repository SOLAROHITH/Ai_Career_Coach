import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash", system_instruction="Reply only in valid JSON. Do not include any extra text.")


def extract_json(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]
        return json.loads(json_text)
    except Exception:
        return None

def get_llm_feedback(resume_text: str, job_text: str) -> dict:
    prompt = f"""
    You are an expert AI career advisor. A candidate submitted the following resume:

    --- RESUME ---
    {resume_text}

    They are applying for this job:

    --- JOB DESCRIPTION ---
    {job_text}

    Please evaluate:
    1. Whether they are a good match
    2. Which skills align well
    3. Which required skills seem missing
    4. How they could improve their resume to match better

    Respond ONLY in JSON like this:
    {{
        "match_strength": "...",
        "missing_skills": [...],
        "llm_explanation": "..."
    }}
    """

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        parsed = extract_json(content)

        if parsed:
            return parsed
        else:
            return {
                "llm_explanation": "Could not extract valid JSON from Gemini response.",
                "raw_output": content
            }

    except Exception as e:
        return {
            "llm_explanation": "Failed to get or parse response from Gemini",
            "error": str(e)
        }
