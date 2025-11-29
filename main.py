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

from pydantic import BaseModel

# -------------------------------
# Soil Input Schema
# -------------------------------
class SoilData(BaseModel):
    ph: float
    nitrogen: float
    phosphorus: float
    potassium: float
    moisture: float


# -------------------------------
# Soil Analysis Endpoint
# -------------------------------
@app.post("/soil")
def analyze_soil(data: SoilData):

    score = (
        (7 - abs(data.ph - 7)) * 10 +
        data.nitrogen +
        data.phosphorus +
        data.potassium +
        data.moisture
    ) / 5

    grade = "Excellent" if score >= 80 else \
            "Good" if score >= 60 else \
            "Moderate" if score >= 40 else \
            "Poor"

    recommendations = []

    if data.ph < 6:
        recommendations.append("Add lime to improve soil pH")
    elif data.ph > 8:
        recommendations.append("Add organic compost to reduce alkalinity")

    if data.nitrogen < 50:
        recommendations.append("Apply urea or vermicompost")

    if data.phosphorus < 40:
        recommendations.append("Apply single super phosphate (SSP)")

    if data.potassium < 40:
        recommendations.append("Apply potash fertilizer")

    if data.moisture < 30:
        recommendations.append("Increase irrigation")

    return {
        "score": round(score, 2),
        "grade": grade,
        "recommendations": recommendations
    }


from pydantic import BaseModel

# -------------------------------
# Fertilizer Input Schema
# -------------------------------

class FertilizerData(BaseModel):
    crop: str
    nitrogen: float
    phosphorus: float
    potassium: float
    soil_grade: str


# -------------------------------
# Fertilizer AI Endpoint
# -------------------------------

@app.post("/fertilizer")
def recommend_fertilizer(data: FertilizerData):

    rec = []

    if data.nitrogen < 50:
        rec.append("Apply Urea - 45 kg per acre")

    if data.phosphorus < 40:
        rec.append("Apply SSP - 35 kg per acre")

    if data.potassium < 40:
        rec.append("Apply Potash - 25 kg per acre")

    if not rec:
        rec.append("NPK levels sufficient — no fertilizer needed")

    organic = "Add Vermicompost (250 kg per acre)"
    safety = "Use gloves & mask during application"

    return {
        "crop": data.crop,
        "recommendations": rec,
        "organic_option": organic,
        "safety_note": safety
    }
