import openai
import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=api_key)
    return client
