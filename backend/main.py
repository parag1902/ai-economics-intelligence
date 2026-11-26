from fastapi import FastAPI
from backend.api.forecast import router as forecast_router

app = FastAPI(
    title="AI Economics Intelligence",
    description="AI-powered cost forecasting and optimization platform",
    version="1.0.0"
)

app.include_router(forecast_router)


@app.get("/")
def home():
    return {
        "message": "AI Economics Intelligence API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }