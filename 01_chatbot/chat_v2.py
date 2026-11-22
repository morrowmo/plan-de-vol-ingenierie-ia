# Chapitre 6 : donner à Nova une mémoire (l’historique de conversation)
# et une fiche de poste (le rôle système).
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"

# Le carnet que l’on tend au poisson rouge à chaque fois.
# La première page est la fiche de poste : le message système.
history = [
    {
        "role": "system",
        "content": (
            "You are Nova, the friendly assistant of Café Comet, a small neighbourhood café. "
            "Answer in two sentences at most. If you don't know something about the café, say so."
        ),
    }
]


def chat(user_message):
    history.append({"role": "user", "content": user_message})       # 1. on note la question
    response = client.chat.completions.create(
        model=MODEL,
        messages=history,                                           # 2. on envoie TOUT le carnet
        temperature=0.7,
        max_tokens=400,
        reasoning_effort="low",  # gpt-oss « réfléchit » avant de répondre : réflexion courte
    )
    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})         # 3. on note aussi la réponse
    return reply


print("Nova is ready. Type 'bye' to leave.")
while True:
    user_message = input("You: ")
    if user_message.lower() in ["bye", "quit", "exit"]:
        print("Nova: See you soon at Café Comet!")
        break
    print("Nova:", chat(user_message))
