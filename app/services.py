import uuid
import time
import json
from app.utils.file_parser import extract_text_from_file
from app.utils.openai_client import analyze_text_with_openai
from app.utils.annotator import annotate_contract
from fastapi import UploadFile, HTTPException

async def analyze_contract(file: UploadFile, language: str = "en") -> dict:
    start_time = time.time()

    # 1. Extraction du texte original
    text = extract_text_from_file(file)

    # 2. Appel à OpenAI
    raw_response = await analyze_text_with_openai(text, language)

    # 3. Nettoyage + Parsing
    if isinstance(raw_response, dict):
        analysis_json = raw_response
    else:
        cleaned_response = clean_openai_response(raw_response)
        try:
            analysis_json = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors du parsing de la réponse OpenAI: {str(e)}")

    # 4. Gestion du score
    risk_score = extract_global_risk_score(analysis_json)
    risk_color = determine_risk_color(risk_score)
    risk_label = determine_risk_label(risk_score)

    # 5. Annotation automatique du texte original
    annotated_text = annotate_contract(text, analysis_json.get("sensitive_clauses", []))

    # 6. Chronométrage
    elapsed_time = round(time.time() - start_time, 2)

    # 7. Construction réponse finale
    return {
        "id": str(uuid.uuid4()),
        "language": language,
        "elapsed_time_seconds": elapsed_time,
        "analysis": {
            **analysis_json,
            "risk_color": risk_color,
            "risk_label": risk_label
        },
        "annotated_text": annotated_text
    }

def clean_openai_response(response_text: str) -> str:
    """Nettoie la réponse OpenAI pour enlever les ```json ``` éventuels."""
    if not isinstance(response_text, str):
        return response_text
    response_text = response_text.strip()
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    return response_text.strip()

def extract_global_risk_score(analysis_json: dict) -> int:
    """Extrait et valide le score global de risque."""
    score_raw = analysis_json.get("global_risk_score", "0")
    try:
        return int(score_raw)
    except ValueError:
        return 0

def determine_risk_color(score: int) -> str:
    """Détermine une couleur basée sur le score de risque."""
    if score <= 30:
        return "green"
    elif 31 <= score <= 60:
        return "orange"
    else:
        return "red"

def determine_risk_label(score: int) -> str:
    """Détermine un label lisible basé sur le score de risque."""
    if score <= 30:
        return "Faible"
    elif 31 <= score <= 60:
        return "Modéré"
    else:
        return "Élevé"


