# Chapitre 5 : une fonction de chat, ses paramètres et une boucle de conversation.
# Remarque : cette version n’a encore AUCUNE mémoire. Demandez-lui « what did I just say? »
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"


def chat(user_message):
    """Envoie un message au LLM et renvoie sa réponse sous forme de texte."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_message}],
        temperature=0.7,         # le curseur d’épices : 0 = sobre et reproductible, 1+ = créatif
        max_tokens=400,          # la taille de la carte postale, réflexion comprise
        reasoning_effort="low",  # gpt-oss « réfléchit » avant de répondre : on garde ça court
        top_p=1.0,               # 1.0 = tous les mots probables (n’y touchez pas au début)
    )
    return response.choices[0].message.content


print("Nova is ready. Type 'bye' to leave.")
while True:
    user_message = input("You: ")
    if user_message.lower() in ["bye", "quit", "exit"]:
        print("Nova: See you soon at Café Comet!")
        break
    print("Nova:", chat(user_message))
