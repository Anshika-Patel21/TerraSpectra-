from fastapi import FastAPI

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