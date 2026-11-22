# Chapitre 9 : trier les avis du Café Comet avec un LLM et un prompt bien écrit.
import csv
import os
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"
DATA = Path(__file__).parent.parent / "data"  # le dossier data, d’où que vous lanciez le script

# Un prompt few-shot : des consignes claires + trois exemples, comme pour former un intérimaire.
SYSTEM_PROMPT = """You sort customer reviews for a café.
Reply with exactly ONE word: positive, negative or neutral.
- positive: the customer is happy
- negative: the customer is unhappy or complains
- neutral: a fact, with no feeling either way

Examples:
Review: "Lovely staff, I'll be back!" -> positive
Review: "My tea was cold." -> negative
Review: "They close at 6 pm." -> neutral"""


def classify(review):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f'Review: "{review}" ->'},
        ],
        temperature=0,  # trier n’est pas un travail créatif : on veut la même réponse à chaque fois
        max_tokens=300,  # de la place pour la courte réflexion du modèle + un mot
        reasoning_effort="low",  # gpt-oss « réfléchit » avant de répondre : réflexion courte
    )
    label = response.choices[0].message.content.strip().lower().strip(".")
    if label not in ["positive", "negative", "neutral"]:
        label = "unknown"  # ne jamais faire confiance au modèle les yeux fermés
    return label


with open(DATA / "reviews.csv", encoding="utf-8") as file:
    reviews = [row["review"] for row in csv.DictReader(file)]

counts = Counter()
for review in reviews:
    label = classify(review)
    counts[label] += 1
    print(f"{label:<9} | {review}")

print("\nSummary:", dict(counts))
