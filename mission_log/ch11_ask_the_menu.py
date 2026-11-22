# Journal de bord, chapitre 11 : chercher dans le menu en boucle, et afficher le prix
# de chaque produit.
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

DATA = Path(__file__).parent.parent / "data"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

with open(DATA / "menu.json", encoding="utf-8") as file:
    menu = json.load(file)

texts = [f"{item['name']}: {item['description']}" for item in menu]
menu_embeddings = model.encode(texts)


def search(question, top_k=3):
    question_embedding = model.encode(question)
    scores = model.similarity(question_embedding, menu_embeddings)[0]
    best = scores.argsort(descending=True)[:top_k]
    # Renvoyer le produit entier (nom, prix, description), pas seulement son nom.
    return [(menu[i], float(scores[i])) for i in best]


print("Search the Café Comet menu. Type 'bye' to leave.")
while True:
    question = input("You: ")
    if question.lower() in ["bye", "quit", "exit"]:
        break
    for item, score in search(question):
        print(f"   {score:.2f}  {item['name']:<20} {item['price']:.2f} €")
