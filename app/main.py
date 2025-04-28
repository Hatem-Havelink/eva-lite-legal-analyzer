from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ TEMPORAIRE pour tester. Après, on restreindra à lovableproject.com
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI(
    title="EVA Lite - Legal Analyzer",
    description="Upload your contract and get an instant analysis!",
    version="1.0"
)

app.include_router(router, prefix="/api")
