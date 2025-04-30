import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_prompt(language: str) -> str:
    if language == "fr":
        return (
            "Tu es un avocat expert en droit des affaires, RGPD et droit contractuel français et européen. "
            "Tu dois analyser un contrat fourni en texte brut et en extraire une synthèse juridique structurée.\n\n"
            "🧠 Ta réponse doit obligatoirement être un JSON strictement conforme à cette structure :\n"
            "{\n"
            "  \"summary\": \"Résumé du contrat en une ou deux phrases\",\n"
            "  \"obligations\": [\"Obligations clés imposées à la partie réceptrice\"],\n"
            "  \"risks\": {\n"
            "    \"major\": [\"Risque important justifié par un article de loi ou jurisprudence\"],\n"
            "    \"medium\": [\"Risque moyen identifié avec justification légale\"],\n"
            "    \"minor\": [\"Risque faible ou technique avec justification légale\"]\n"
            "  },\n"
            "  \"sensitive_clauses\": [\n"
            "    {\n"
            "      \"clause\": \"Nom ou thème de la clause (ex : Non-concurrence)\",\n"
            "      \"commentary\": \"Pourquoi elle est critique, et base légale ou jurisprudence associée\"\n"
            "    }\n"
            "  ],\n"
            "  \"global_risk_score\": \"Score de risque global entre 0 et 100\",\n"
            "  \"risk_color\": \"green | orange | red\",\n"
            "  \"risk_label\": \"Faible | Modéré | Élevé\"\n"
            "}\n\n"
            "🧷 Pour chaque risque ou clause sensible, ajoute une justification :\n"
            "- Soit un article de loi (ex : Article 1134 Code civil, Article 6 RGPD…)\n"
            "- Soit une jurisprudence (ex : Cass. com., 10 juillet 2007, n°06-14.006)\n\n"
            "🚫 Ta réponse doit être strictement du JSON, sans aucune explication, sans balises markdown (pas de ```json)."
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



