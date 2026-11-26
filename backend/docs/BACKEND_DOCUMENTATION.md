# TerraSpectra – Backend Documentation

## 1. Project Overview

TerraSpectra is a grapevine disease detection project that combines
machine learning and geospatial data processing.

The backend provides API endpoints for image-based disease prediction
and raster metadata inspection.

## 2. Backend Responsibilities

The backend is responsible for:

- Providing REST API endpoints using FastAPI.
- Loading the trained MobileNetV2 model.
- Processing uploaded leaf images.
- Generating disease classification predictions.
- Returning prediction confidence and class probabilities.
- Inspecting uploaded geospatial raster files.
- Handling invalid and empty file uploads.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| TensorFlow | Deep learning inference |
| MobileNetV2 | Image classification |
| NumPy | Numerical operations |
| Rasterio | Raster metadata inspection |
| Pydantic | Data validation |
| Uvicorn | ASGI server |

## 4. Project Structure

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── services/
│   │   ├── model_adapter.py
│   │   ├── raster_service.py
│   │   └── prediction_service.py
│   │
│   └── schemas/
│       └── prediction.py
│
├── models/
│   └── terraspectra_mobilenetv2_final.keras
│
├── tests/
│   ├── test_model_adapter.py
│   └── test_raster_service.py
│
├── requirements.txt
└── docs/
    └── BACKEND_DOCUMENTATION.md