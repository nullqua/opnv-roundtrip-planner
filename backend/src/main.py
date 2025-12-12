from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "ÖPNV Roundtrip Planner API",
    description = "API for calculating roundtrip routes using public transportation",
    version = "0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def read_root():
    """Health check endpoint"""
    return {"message": "ÖPNV Roundtrip Planner API",
            "status": "running",
            "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "backend"
    }
