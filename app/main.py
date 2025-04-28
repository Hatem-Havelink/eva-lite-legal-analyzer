from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router

app = FastAPI(  # <-- il faut d'abord créer l'instance FastAPI ici
    title="Eva Lite - Analyse juridique automatique",
    description="API pour l'analyse juridique automatique de contrats (PDF, DOCX) via FastAPI et OpenAI.",
    version="1.0.0"
)

# ➔ Ensuite seulement tu ajoutes le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["ttps://fa03942d-5fe6-4f5f-8a53-fcb78e3dcfac.lovableproject.com"],  # On ouvre à tout pour tests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ➔ Puis tu inclus les routes
app.include_router(router, prefix="/api")
