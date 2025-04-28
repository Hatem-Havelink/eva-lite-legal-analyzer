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
    allow_origin_regex=r"https://.*\.loveableproject\.com|http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ➔ Puis tu inclus les routes
app.include_router(router, prefix="/api")
