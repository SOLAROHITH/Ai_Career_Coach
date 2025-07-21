from fastapi import FastAPI,File,UploadFile
from resume_parser import extract_text_from_pdf

app = FastAPI()


@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text_from_pdf(content)
    return {"extracted_text": text}
