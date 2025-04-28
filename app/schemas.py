from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

# --- Enum pour la langue ---
class LanguageEnum(str, Enum):
    fr = "fr"
    en = "en"

# --- Modèles pour l'analyse ---
class RiskAnalysis(BaseModel):
    major: List[str]
    minor: List[str]

class SensitiveClause(BaseModel):
    clause: str
    commentary: str

class ContractAnalysis(BaseModel):
    summary: str
    obligations: List[str]
    risks: RiskAnalysis
    sensitive_clauses: List[SensitiveClause]
    global_risk_score: str
    risk_color: Optional[str] = None
    risk_label: Optional[str] = None

# --- Modèle principal de réponse ---
class ContractAnalysisResponse(BaseModel):
    id: str
    language: LanguageEnum
    elapsed_time_seconds: float
    analysis: ContractAnalysis
    annotated_text: Optional[str] = None  # ➔ On ajoute ici l'annotation propre


