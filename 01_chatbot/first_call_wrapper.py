# Chapitre 4 : le même message, via la « télécommande universelle » d’OpenAI.
# De nombreux fournisseurs (Groq, Mistral, Together, Ollama...) comprennent ce format :
# changer de fournisseur revient donc à changer seulement base_url, api_key et MODEL.
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)
MODEL = "openai/gpt-oss-120b"  # le nom du modèle chez Groq (voir console.groq.com/docs/models)

response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Say hello to the Café Comet team in one sentence."}],
)

print(response.choices[0].message.content)
