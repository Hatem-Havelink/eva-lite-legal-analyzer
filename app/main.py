from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="EVA Lite - Legal Analyzer",
    description="Upload your contract and get an instant analysis!",
    version="1.0"
)

app.include_router(router, prefix="/api")
