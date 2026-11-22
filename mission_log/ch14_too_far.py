# Journal de bord, chapitre 14 : afficher les fiches trouvées par Nova, et ne même pas
# appeler le LLM
# quand la meilleure fiche est trop éloignée de la question.
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

load_dotenv()
DB_FOLDER = Path(__file__).parent.parent / "04_rag" / "chroma_db"
llm = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"
MAX_DISTANCE = 0.8  # 0 = même direction ; plus c’est loin, moins c’est lié

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
collection = chromadb.PersistentClient(path=str(DB_FOLDER)).get_collection("cafe_handbook")


def retrieve(question, top_k=3):
    results = collection.query(query_embeddings=embedder.encode([question]).tolist(), n_results=top_k)
    return results["documents"][0], results["metadatas"][0], results["distances"][0]


def answer(question):
    cards, sources, distances = retrieve(question)
    for source, distance in zip(sources, distances):
        print(f"   [{distance:.2f}] {source['source']}")
    if distances[0] > MAX_DISTANCE:  # même la meilleure fiche est loin : inutile de demander au LLM
        return "I don't know, please ask a member of staff."
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
