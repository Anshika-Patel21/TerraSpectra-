import os
import tempfile

from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException

from app.services.prediction_service import generate_mock_prediction
from app.schemas.prediction import PredictionRequest
from app.services.raster_service import inspect_raster

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
#@app.post("/predict")
#def predict(request: PredictionRequest):

 #   return {
  #      "message": "Prediction request received successfully",
   #     "farm_id": request.farm_id,
    #    "file_name": request.file_name,
     #   "status": "pending"
    #}
@app.post("/predict")
def predict(request: PredictionRequest):
    result = generate_mock_prediction(
        farm_id=request.farm_id,
        file_name=request.file_name
    )

    return result

@app.post("/inspect-raster")
async def inspect_raster_endpoint(file: UploadFile = File(...)):

    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    suffix = Path(file.filename or "upload.tif").suffix or ".tif"

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(contents)
            temp_path = temp.name

        metadata = inspect_raster(temp_path)

        return {
            "message": "Raster inspection successful",
            "filename": file.filename,
            "metadata": metadata
        }

    except (ValueError, OSError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
