import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_text_with_openai(text: str, language: str):
    if language == "fr":
        instruction = (
            "Tu es un expert juridique. Analyse le document fourni et retourne uniquement un JSON brut sans balises ``` ni explication."
            "Le JSON doit suivre cette structure :\n"
            "{\n"
            "  \"summary\": \"Résumé concis du contrat.\",\n"
            "  \"obligations\": [\"Liste des obligations principales\"],\n"
            "  \"risks\": {\n"
            "    \"major\": [\"Liste des risques majeurs\"],\n"
            "    \"minor\": [\"Liste des risques mineurs\"]\n"
            "  },\n"
            "  \"sensitive_clauses\": [\n"
            "    {\n"
            "      \"clause\": \"Titre ou sujet de la clause\",\n"
            "      \"commentary\": \"Explication du risque ou impact.\"\n"
            "    }\n"
            "  ],\n"
            "  \"global_risk_score\": \"Score de risque global entre 0 et 100\"\n"
            "}\n"
            "IMPORTANT : Ne mets **aucun** ```json ou ``` dans ta réponse."
        )
    else:
        instruction = (
            "You are a legal expert. Analyze the document and return only raw JSON, without any ```json or ``` markers."
            "The JSON must follow this structure:\n"
            "{\n"
            "  \"summary\": \"Concise summary.\",\n"
            "  \"obligations\": [\"List of obligations\"],\n"
            "  \"risks\": {\n"
            "    \"major\": [\"List of major risks\"],\n"
            "    \"minor\": [\"List of minor risks\"]\n"
            "  },\n"
            "  \"sensitive_clauses\": [\n"
            "    {\"clause\": \"Clause title\", \"commentary\": \"Explanation\"}\n"
            "  ],\n"
            "  \"global_risk_score\": \"Score between 0 and 100\"\n"
            "}\n"
            "IMPORTANT: No ```json or ``` markers around your response."
        )

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": text}
        ],
        temperature=0.2,
    )
    content = response.choices[0].message.content.strip()

    # Nettoyage si jamais il reste quand même des ``` par sécurité
    if content.startswith("```") and content.endswith("```"):
        content = content.strip("`").strip()

    try:
        # On parse le texte proprement en JSON Python
        json_content = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Erreur de parsing JSON dans la réponse d'OpenAI.")

    return json_content


