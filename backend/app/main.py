from fastapi import FastAPI
from app.schemas.prediction import PredictionRequest

app = FastAPI(
    title="TerraSpectra API",
    description="Backend service for hyperspectral crop stress detection",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to TerraSpectra API",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "TerraSpectra"
    }
@app.post("/predict")
def predict(request: PredictionRequest):

    return {
        "message": "Prediction request received successfully",
        "farm_id": request.farm_id,
        "file_name": request.file_name,
        "status": "pending"
    }