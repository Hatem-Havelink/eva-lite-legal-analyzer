import json
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def call_openai(prompt: str, content: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
def get_prompts(language: str) -> dict:
    if language == "fr":
        return {
            "summary": "Tu es un juriste. Donne un résumé clair (5 lignes max) du contrat ci-dessous. Aucun commentaire.",
            "obligations": "Liste les obligations principales de la partie réceptrice, en phrases simples.",
            "risks": "Identifie les risques juridiques du contrat, classés en majeur / moyen / mineur, avec justification (article de loi ou jurisprudence).",
            "clauses": "Identifie les clauses sensibles (ex: non-concurrence, données, responsabilité) avec commentaire juridique. Donne aussi un score global de risque de 0 à 100, un label (Faible / Modéré / Élevé) et une couleur (green/orange/red)."
        }
    else:
        raise NotImplementedError("English version not yet implemented.")
async def analyze_contract_in_parts(text: str, language: str):
    prompts = get_prompts(language)

    summary = await call_openai(prompts["summary"], text)
    obligations = await call_openai(prompts["obligations"], text)
    risks = await call_openai(prompts["risks"], text)
    clauses_json = await call_openai(prompts["clauses"], text)

    # Parsage du dernier bloc (qui contient du JSON)
    clauses_data = json.loads(clauses_json)

    return {
        "summary": summary,
        "obligations": obligations.split("\n"),
        "risks": clauses_data.get("risks", {}),
        "sensitive_clauses": clauses_data.get("sensitive_clauses", []),
        "global_risk_score": clauses_data.get("global_risk_score", "50"),
        "risk_color": clauses_data.get("risk_color", "orange"),
        "risk_label": clauses_data.get("risk_label", "Modéré")
    }
