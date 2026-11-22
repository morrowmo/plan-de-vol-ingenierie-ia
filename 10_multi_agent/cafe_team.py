# Chapitre 24 : une équipe d’agents avec un superviseur (le chef de cuisine).
# Chaque spécialiste est un agent avec ses propres outils. Le superviseur voit les spécialistes
# comme des outils : il lit la demande, confie chaque partie au bon spécialiste, puis répond.
import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from sentence_transformers import SentenceTransformer

sys.path.append(str(Path(__file__).parent.parent / "05_agent"))
from cafe_tools import get_menu, get_weather  # noqa: E402  (nos outils de la Planète Agent)

load_dotenv()
# max_retries : si l’offre gratuite répond « trop de tokens par minute »,
# on attend et on réessaie (jusqu’à 6 fois)
MODEL = init_chat_model("groq:openai/gpt-oss-120b", max_retries=6)

# --- Un outil pour le spécialiste du support : chercher dans la bibliothèque du manuel
# (Planète RAG) ---
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
handbook = chromadb.PersistentClient(path=str(Path(__file__).parent.parent / "04_rag" / "chroma_db")).get_collection("cafe_handbook")


@tool
def search_handbook(question: str) -> str:
    """Search the Café Comet staff handbook (hours, allergens, loyalty card, pets, events, staff rules)."""
    results = handbook.query(query_embeddings=embedder.encode([question]).tolist(), n_results=3)
    return "\n\n".join(results["documents"][0])


# --- Les cuisiniers : un poste chacun ---
orders_agent = create_agent(MODEL, tools=[get_menu],
    system_prompt="You handle orders for Café Comet. Use the menu to list items and compute totals in euros.")
marketing_agent = create_agent(MODEL, tools=[get_weather, get_menu],
    system_prompt="You write short, friendly marketing ideas for Café Comet in Lyon. Check the weather first. "
                  "Only use items that are on the menu, at their exact menu price.")
support_agent = create_agent(MODEL, tools=[search_handbook],
    system_prompt="You answer customer questions about Café Comet using ONLY the handbook. Say if you don't know.")


# --- Le superviseur voit chaque cuisinier comme un outil ---
@tool
def ask_orders(request: str) -> str:
    """Send an order or price question to the orders specialist."""
    print("   [supervisor -> orders]")
    return orders_agent.invoke({"messages": [{"role": "user", "content": request}]})["messages"][-1].content


@tool
def ask_marketing(request: str) -> str:
    """Send a marketing, social media or specials-board request to the marketing specialist."""
    print("   [supervisor -> marketing]")
    return marketing_agent.invoke({"messages": [{"role": "user", "content": request}]})["messages"][-1].content


@tool
def ask_support(request: str) -> str:
    """Send a question about café rules, hours, allergens, loyalty or pets to the support specialist."""
    print("   [supervisor -> support]")
    return support_agent.invoke({"messages": [{"role": "user", "content": request}]})["messages"][-1].content


supervisor = create_agent(
    MODEL,
    tools=[ask_orders, ask_marketing, ask_support],
    system_prompt=(
        "You are the head of Café Comet's assistant team. Split the manager's request into parts, "
        "send each part to the right specialist, then combine their answers into one clear reply. "
        "Never invent facts yourself. Reply in plain text, no tables."
    ),
)

if __name__ == "__main__":
    request = input("Manager's request (or press Enter for the example): ") or (
        "A customer wants 3 croissants and 2 cappuccinos: how much is it? "
        "Also, can they bring their dog? And give me one idea for today's specials board."
    )
    result = supervisor.invoke({"messages": [{"role": "user", "content": request}]})
    print("\nNova's team:", result["messages"][-1].content)
