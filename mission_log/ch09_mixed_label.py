# Journal de bord, chapitre 9 : une quatrième étiquette, « mixed », pour les avis
# à la fois contents et mécontents.
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"
LABELS = ["positive", "negative", "neutral", "mixed"]

SYSTEM_PROMPT = """You sort customer reviews for a café.
Reply with exactly ONE word: positive, negative, neutral or mixed.
- positive: the customer is happy
- negative: the customer is unhappy or complains
- neutral: a fact, with no feeling either way
- mixed: the customer is happy about one thing and unhappy about another

Examples:
Review: "Lovely staff, I'll be back!" -> positive
Review: "My tea was cold." -> negative
Review: "They close at 6 pm." -> neutral
Review: "Great cake, but the music was far too loud." -> mixed"""


def classify(review):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f'Review: "{review}" ->'},
        ],
        temperature=0,
        max_tokens=300,
        reasoning_effort="low",
    )
    label = response.choices[0].message.content.strip().lower().strip(".")
    if label not in LABELS:
        label = "unknown"
    return label


tests = [
    "The coffee was excellent but the waiter was rude.",
    "Delicious croissant, terrible queue.",
    "Best hot chocolate in town, my kids love it.",
    "They have Wi-Fi.",
]
for review in tests:
    print(f"{classify(review):<9} | {review}")
