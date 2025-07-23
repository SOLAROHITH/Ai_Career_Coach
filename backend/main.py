from fastapi import FastAPI,File,UploadFile, HTTPException
from resume_parser import extract_text_from_pdf
from pydantic import BaseModel      
from matcher import get_similarity_score
from llm_reasoner import get_llm_feedback
from db import insert_job, fetch_all_jobs

app = FastAPI()

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text_from_pdf(content)
    return {"extracted_text": text}


class MatchRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/match-resume/")
def match_resume(request: MatchRequest):
    resume = request.resume_text
    job = request.job_description

    # Step 1: Embedding similarity score
    similarity = get_similarity_score(resume, job)

    # Step 2: GPT-based reasoning
    llm_data = get_llm_feedback(resume, job)

    return {
        "similarity": similarity,
        **llm_data  # merges fields like match_strength, missing_skills, etc.
    }
class JobIn(BaseModel):
    title: str
    company: str = None
    location: str = None
    description: str

@app.post("/add_job")
def add_job(job: JobIn):
    insert_job(job.title, job.company, job.location, job.description)
    return {"status": "Job added successfully"}

@app.post("/match-jobs/")
async def match_jobs(resume: UploadFile = File(...), threshold: float = 0.3):
    # Step 1: Extract resume text
    resume_text = await resume.read()
    resume_text = extract_text_from_pdf(resume_text)

    # Step 2: Fetch jobs from DB
    jobs = fetch_all_jobs()

    # Step 3: Match each job
    matched_jobs = []
    for job in jobs:
        job_id, title, company, location, description = job
        score = get_similarity_score(resume_text, description)
        if score >= threshold:
            matched_jobs.append({
                "job_id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "similarity": score
            })

    # Step 4: Return matched jobs
    return {"matches": sorted(matched_jobs, key=lambda x: x["similarity"], reverse=True)}