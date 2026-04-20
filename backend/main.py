from fastapi import FastAPI, UploadFile
app = FastAPI()

@app.post("/score_resume")
async def score_resume(file: UploadFile):
    text = await file.read()
    # placeholder scoring logic
    return {"score": len(text) % 100}
