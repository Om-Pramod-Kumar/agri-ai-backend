from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "Backend working",
        "message": "NeoKrishi API is live"
    }

@app.post("/pest")
async def pest_detect(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "disease": "Leaf Blast",
        "confidence": "87%"
    }
