import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_prompt(language: str) -> str:
    if language == "fr":
        return (
            "Tu es un expert juridique en droit français et européen. Tu dois analyser un contrat transmis intégralement dans le message utilisateur. "
            "Ton objectif est de produire un fichier JSON structuré, utile à une entreprise pour identifier les risques, obligations, et clauses sensibles. "
            "Ta réponse doit être un **JSON brut**, sans balises markdown (PAS de ```json ou autre)."

            "Voici la structure du JSON attendu :\n"
            "{\n"
            "  \"summary\": \"Résumé concis du contrat (4-6 lignes).\",\n"
            "  \"obligations\": [\"Liste des principales obligations de la partie réceptrice.\", \"...\"],\n"
            "  \"risks\": {\n"
            "    \"major\": [\"Risque majeur avec justification par article de loi ou jurisprudence.\"],\n"
            "    \"medium\": [\"Risque moyen avec justification.\"],\n"
            "    \"minor\": [\"Risque faible mais existant.\"]\n"
            "  },\n"
            "  \"sensitive_clauses\": [\n"
            "    {\n"
            "      \"clause\": \"Nom ou nature de la clause (ex: Non-Concurrence)\",\n"
            "      \"commentary\": \"Explication du risque ou du déséquilibre juridique, avec référence au droit applicable.\"\n"
            "    }\n"
            "  ],\n"
            "  \"global_risk_score\": \"Score de risque global entre 0 et 100 (voir ci-dessous)\",\n"
            "  \"risk_color\": \"green/orange/red\",\n"
            "  \"risk_label\": \"Faible / Modéré / Élevé\"\n"
            "}\n\n"
            "Pour calculer le 'global_risk_score', utilise cette grille indicative :\n"
            "- Base de 20 points (risque nul)\n"
            "- +10 si au moins une clause sensible est identifiée\n"
            "- +10 si une clause non-concurrentielle ou non-sollicitation déséquilibrée\n"
            "- +10 si plusieurs obligations excessives\n"
            "- +10 si manque de réciprocité\n"
            "- +10 à 30 si risques juridiques majeurs (ex : non-respect RGPD, dépendance unilatérale, confidentialité abusive)\n"
            "- Maximum = 100\n\n"
            "IMPORTANT : Ne produis **aucun commentaire** en dehors du JSON."
        )
    else:
        return (
            "You are a legal expert specialized in EU and French commercial and privacy law. "
            "Analyze the raw contract text and return a structured legal summary in strict JSON format.\n\n"
            "Your JSON must follow this structure:\n"
            "{\n"
            "  \"summary\": \"Brief summary of the contract\",\n"
            "  \"obligations\": [\"Key obligations\"],\n"
            "  \"risks\": {\n"
            "    \"major\": [\"Major risk justified by a legal article or case law\"],\n"
            "    \"medium\": [\"Medium risk justified\"],\n"
            "    \"minor\": [\"Minor technical or compliance risk\"]\n"
            "  },\n"
            "  \"sensitive_clauses\": [\n"
            "    {\"clause\": \"Clause name\", \"commentary\": \"Explanation + legal base\"}\n"
            "  ],\n"
            "  \"global_risk_score\": \"Score from 0 to 100\",\n"
            "  \"risk_color\": \"green | orange | red\",\n"
            "  \"risk_label\": \"Low | Medium | High\"\n"
            "}\n\n"
            "Each clause or risk **must be justified** with either:\n"
            "- a legal article (e.g. Article 6 GDPR, Article 1134 French Civil Code)\n"
            "- or a court decision (e.g. ECJ, Cass. com. July 10, 2007, no. 06-14.006)\n\n"
            "Return ONLY pure JSON — no explanations, no markdown code blocks."
        )

async def analyze_text_with_openai(text: str, language: str):
    prompt = get_prompt(language)

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    # Nettoyage sécurité
    if content.startswith("```"):
        content = content.strip("`").strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Erreur de parsing JSON dans la réponse d'OpenAI.")
