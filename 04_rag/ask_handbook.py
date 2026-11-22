# Chapitre 14 : l’examen à livre ouvert. Trouver les meilleures fiches,
# puis laisser le LLM répondre à partir d’elles.
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

load_dotenv()
DB_FOLDER = Path(__file__).parent / "chroma_db"
llm = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # le MÊME modèle qu’à la construction
collection = chromadb.PersistentClient(path=str(DB_FOLDER)).get_collection("cafe_handbook")


def retrieve(question, top_k=3):
    """R comme Récupération (Retrieval) : demander à la bibliothécaire les meilleures fiches."""
    results = collection.query(query_embeddings=embedder.encode([question]).tolist(), n_results=top_k)
    return results["documents"][0], results["metadatas"][0]


def answer(question):
    """G comme Génération : le LLM répond en s’appuyant UNIQUEMENT sur les fiches trouvées."""
    cards, sources = retrieve(question)
    context = "\n\n".join(f"[{s['source']}] {card}" for card, s in zip(cards, sources))
    response = llm.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": (
                "You are Nova, the assistant of Café Comet. Answer the question using ONLY the "
                "handbook extracts below. If the answer is not in them, say: \"I don't know, "
                "please ask a member of staff.\" When you do answer, mention the source file in brackets.\n\n"
                f"Handbook extracts:\n{context}"
            )},
            {"role": "user", "content": question},
        ],
        temperature=0,
        reasoning_effort="low",
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print("Ask Nova about the café handbook. Type 'bye' to leave.")
    while True:
        question = input("You: ")
        if question.lower() in ["bye", "quit", "exit"]:
            break
        print("Nova:", answer(question))
