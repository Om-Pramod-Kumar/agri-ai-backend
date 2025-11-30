from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io
from pydantic import BaseModel

# --------------------------------------
# APP INIT
# --------------------------------------
app = FastAPI()

# --------------------------------------
# BASIC TEST ROUTE
# --------------------------------------
@app.get("/")
def home():
    return {
        "status": "Backend working",
        "message": "NeoKrishi API is live"
    }

# -------------------------------------
# LOAD TRAINED PEST MODEL
# -------------------------------------
model = load_model("pest_model.keras")

CLASS_NAMES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___healthy",
    "Potato___Late_blight",
    "Tomato___Target_Spot",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___Tomato_YellowLeaf_Curl_Virus",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___healthy",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites",
    "Tomato___Two-spotted_spider_mite"
]

# -------------------------------------
# IMAGE PREPROCESSOR
# -------------------------------------
def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224,224))
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, axis=0)


# -------------------------------------
# 🐛 PEST AI ENDPOINT
# -------------------------------------
@app.post("/pest")
async def diagnose(file: UploadFile = File(...)):
    image_bytes = await file.read()
    processed = preprocess_image(image_bytes)

    preds = model.predict(processed)[0]

    idx = np.argmax(preds)
    confidence = float(preds[idx])

    return {
        "filename": file.filename,
        "disease": CLASS_NAMES[idx],
        "confidence": f"{confidence * 100:.2f}%"
    }


# -------------------------------------
# 🌱 SOIL AI
# -------------------------------------
class SoilData(BaseModel):
    ph: float
    nitrogen: float
    phosphorus: float
    potassium: float
    moisture: float


@app.post("/soil")
def analyze_soil(data: SoilData):

    score = (
        (7 - abs(data.ph - 7)) * 10 +
        data.nitrogen +
        data.phosphorus +
        data.potassium +
        data.moisture
    ) / 5

    grade = (
        "Excellent" if score >= 80 else
        "Good" if score >= 60 else
        "Moderate" if score >= 40 else
        "Poor"
    )

    recommendations = []

    if data.ph < 6:
        recommendations.append("Add lime to improve soil pH")
    elif data.ph > 8:
        recommendations.append("Add compost to reduce alkalinity")

    if data.nitrogen < 50:
        recommendations.append("Apply Urea or Vermicompost")

    if data.phosphorus < 40:
        recommendations.append("Apply SSP")

    if data.potassium < 40:
        recommendations.append("Apply Potash")

    if data.moisture < 30:
        recommendations.append("Increase irrigation")

    return {
        "score": round(score, 2),
        "grade": grade,
        "recommendations": recommendations
    }


# -------------------------------------
# 🌾 FERTILIZER AI
# -------------------------------------
class FertilizerData(BaseModel):
    crop: str
    nitrogen: float
    phosphorus: float
    potassium: float
    soil_grade: str


@app.post("/fertilizer")
def recommend_fertilizer(data: FertilizerData):

    rec = []

    if data.nitrogen < 50:
        rec.append("Apply Urea - 45 kg/ac")

    if data.phosphorus < 40:
        rec.append("Apply SSP - 35 kg/ac")

    if data.potassium < 40:
        rec.append("Apply Potash - 25 kg/ac")

    if not rec:
        rec.append("Soil nutrients sufficient")

    return {
        "crop": data.crop,
        "recommendations": rec,
        "organic_option": "Add Vermicompost 250kg/ac",
        "safety_note": "Use gloves & mask while applying"
    }


# -------------------------------------
# 🌿 CROP RECOMMENDATION
# -------------------------------------
class CropData(BaseModel):
    soil_grade: str
    season: str
    temperature: float
    rainfall: str


@app.post("/crop")
def recommend_crop(data: CropData):

    crops = []

    if data.soil_grade == "Excellent":
        crops += ["Wheat","Rice","Sugarcane"]

    elif data.soil_grade == "Good":
        crops += ["Maize","Cotton"]

    elif data.soil_grade == "Moderate":
        crops += ["Millets","Pulses"]

    else:
        crops += ["Barley","Mustard"]

    if data.season.lower() == "summer":
        crops += ["Groundnut","Watermelon"]

    if data.rainfall.lower() == "high":
        crops.append("Paddy")

    return {
        "recommended_crops": list(set(crops)),
        "season": data.season,
        "soil_grade": data.soil_grade
    }


# -------------------------------------
# 📈 MARKET DEMO AI
# -------------------------------------
class MarketRequest(BaseModel):
    crop: str
    mandi: str


@app.post("/market")
def market_prediction(data: MarketRequest):

    base_price = {
        "Wheat": 2150,
        "Rice": 2450,
        "Maize": 1920,
        "Cotton": 6200,
        "Millets": 3200,
        "Pulses": 5400,
        "Vegetables": 3000
    }

    trend_map = {
        "Wheat": "⬆ Increasing",
        "Rice": "➡ Stable",
        "Maize": "⬇ Decreasing",
        "Cotton": "⬆ Increasing",
        "Millets": "➡ Stable",
        "Pulses": "⬆ Increasing",
        "Vegetables": "⬇ Decreasing"
    }

    crop = data.crop

    price = base_price.get(crop, 3000)
    trend = trend_map.get(crop, "➡ Stable")

    prediction_7day = price + 150 if "⬆" in trend else price - 100

    best_sell_day = "Next 3 days" if "⬆" in trend else "Wait 5–7 days"

    return {
        "crop": crop,
        "mandi": data.mandi,
        "today_price": price,
        "price_after_7_days": prediction_7day,
        "market_trend": trend,
        "best_sell_time": best_sell_day
    }
