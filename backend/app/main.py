import os
import tempfile

from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException

from app.services.model_adapter import RealModelAdapter
from app.services.raster_service import inspect_raster


app = FastAPI(
    title="TerraSpectra API",
    description="Backend service for grapevine disease detection",
    version="1.0.0"
)

model_adapter = RealModelAdapter()


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
async def predict(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    suffix = Path(file.filename).suffix.lower()

    if suffix not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG and PNG images are supported"
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Empty image uploaded"
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp:
            temp.write(contents)
            temp_path = temp.name

        result = model_adapter.predict(temp_path)

        result["filename"] = file.filename

        return result

    except (ValueError, FileNotFoundError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/inspect-raster")
async def inspect_raster_endpoint(file: UploadFile = File(...)):

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Empty file uploaded"
        )

    suffix = Path(file.filename or "upload.tif").suffix or ".tif"

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp:
            temp.write(contents)
            temp_path = temp.name

        metadata = inspect_raster(temp_path)

        return {
            "message": "Raster inspection successful",
            "filename": file.filename,
            "metadata": metadata
        }

    except (ValueError, OSError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)