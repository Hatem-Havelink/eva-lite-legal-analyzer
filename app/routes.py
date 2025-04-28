from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services import analyze_contract
from app.schemas import ContractAnalysisResponse, LanguageEnum

router = APIRouter()

MAX_FILE_SIZE_MB = 10  # Limite fixée à 10 Mo

@router.post(
    "/analyze-contract",
    response_model=ContractAnalysisResponse,
    summary="Analyse juridique automatique d'un contrat",
    description="Uploade un document (PDF ou DOCX) et reçois une analyse juridique structurée avec résumé, obligations, risques, clauses sensibles et score de risque global."
)
async def analyze_contract_endpoint(
    file: UploadFile = File(..., description="Document contractuel à analyser (PDF ou DOCX)"),
    language: LanguageEnum = Form(..., description="Langue de l'analyse ('fr' pour Français, 'en' pour Anglais)")
):
    try:
        contents = await file.read()
        file_size_mb = len(contents) / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            raise HTTPException(status_code=400, detail=f"Le fichier dépasse la limite autorisée de {MAX_FILE_SIZE_MB} Mo.")

        file.file.seek(0)

        result = await analyze_contract(file, language.value)
        return result  # ➔ juste return, FastAPI transforme proprement en JSON

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


