from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import pdfplumber
import docx
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

# Enable CORS so React can call FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face models
nlp = pipeline("sentiment-analysis")
embedder = SentenceTransformer("all-MiniLM-L6-v2")  # semantic embeddings

def extract_text(file: UploadFile, content: bytes) -> str:
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            return " ".join([page.extract_text() or "" for page in pdf.pages])
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        return " ".join([para.text for para in doc.paragraphs])
    else:
        return content.decode("utf-8", errors="ignore")

@app.post("/score_resume")
async def score_resume(
    file: UploadFile = File(...),
    jd: str = Form("")   # job description text
):
    content = await file.read()
    resume_text = extract_text(file, content)

    # Resume score (placeholder sentiment)
    result = nlp(resume_text[:500])
    score = result[0]['score'] * 100

    # Semantic similarity for JD matching
    match_percentage = None
    if jd.strip():
        resume_vec = embedder.encode(resume_text, convert_to_tensor=True)
        jd_vec = embedder.encode(jd, convert_to_tensor=True)
        similarity = util.cos_sim(resume_vec, jd_vec).item()
        match_percentage = round(similarity * 100, 2)

    return {
        "resume_score": round(score, 2),
        "feedback": result[0]['label'],
        "match_percentage": match_percentage
    }
