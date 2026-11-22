# Chapitre 11 : la recherche sémantique. Trouver les plats d’après ce que vous VOULEZ DIRE,
# pas d’après les mots exacts.
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

DATA = Path(__file__).parent.parent / "data"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

with open(DATA / "menu.json", encoding="utf-8") as file:
    menu = json.load(file)

# 1. On donne ses coordonnées à chaque produit du menu, une fois pour toutes, avant toute question.
texts = [f"{item['name']}: {item['description']}" for item in menu]
menu_embeddings = model.encode(texts)


def search(question, top_k=3):
    question_embedding = model.encode(question)
    scores = model.similarity(question_embedding, menu_embeddings)[0]  # un score par produit
    best = scores.argsort(descending=True)[:top_k]                     # rangs des meilleurs scores
    return [(menu[i]["name"], float(scores[i])) for i in best]


questions = [
    "a sweet treat for my children",
    "I can't eat wheat",
    "a cold drink for a hot day",
    "something warm without coffee",  # un piège ! voyez ce qui se passe avec le mot « without »
]
for question in questions:
    print(f"\n🔎 {question}")
    for name, score in search(question):
        print(f"   {score:.2f}  {name}")
