# Chapitre 4 : votre tout premier message à un LLM.
# L’InferenceClient de Hugging Face parle à de nombreux fournisseurs. Ici, on choisit Groq.
import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()  # lit GROQ_API_KEY dans le fichier .env

client = InferenceClient(
    provider="groq",                    # le restaurant qui cuisine pour nous
    api_key=os.getenv("GROQ_API_KEY"),  # notre clé de la maison
)

response = client.chat_completion(
    model="openai/gpt-oss-120b",  # le nom du modèle sur Hugging Face
    messages=[{"role": "user", "content": "Say hello to the Café Comet team in one sentence."}],
)

print(response.choices[0].message.content)
