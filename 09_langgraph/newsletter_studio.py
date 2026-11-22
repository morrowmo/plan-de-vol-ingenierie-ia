# Chapitre 23 : un système automatisé de rédaction et de relecture d’articles.
# Un rédacteur écrit un brouillon, un éditeur le relit, et le brouillon fait des allers-retours
# jusqu’à être bon
# (ou jusqu’à MAX_ROUNDS, pour ne jamais tourner sans fin).
import json
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

load_dotenv()
MAX_ROUNDS = 3

# Les faits que le rédacteur peut utiliser. Sans eux, les LLM inventent volontiers
# des plats, des événements et des adresses !
DATA = Path(__file__).parent.parent / "data"
MENU = "\n".join(f"- {item['name']} ({item['price']:.2f} €)"
                 for item in json.loads((DATA / "menu.json").read_text(encoding="utf-8")))
FACTS = f"""Café Comet's real menu:\n{MENU}
Opening hours: Mon-Fri 7:30-18:00, Sat 8:30-19:00, Sun 9:00-14:00.
Board-game evening every first Thursday of the month, 18:30-21:30, free entry. No live music."""

writer_model = init_chat_model("groq:openai/gpt-oss-120b", temperature=0.8, max_retries=6)  # créatif
editor_model = init_chat_model("groq:openai/gpt-oss-120b", temperature=0, max_retries=6)    # strict


class Studio(TypedDict):
    topic: str
    draft: str
    feedback: str
    approved: bool
    rounds: int


class Review(BaseModel):  # l’éditeur remplit ce formulaire (sortie structurée)
    approved: bool = Field(description="True only if the newsletter meets EVERY rule")
    feedback: str = Field(description="Short, concrete changes to make. Empty if approved.")


EDITOR_RULES = """Rules for Café Comet's newsletter:
1. Between 80 and 150 words.
2. A catchy title on the first line.
3. Mentions at least one menu item by name.
4. Ends with a call to action (for example: come and visit).
5. Friendly tone, no exaggerated claims.
6. Uses ONLY the facts given: no invented dishes, prices, events, dates or addresses."""


def write(state: Studio):
    if state["feedback"]:
        prompt = (f"Rewrite this newsletter about '{state['topic']}' for Café Comet.\n{FACTS}\n"
                  f"Editor's feedback: {state['feedback']}\n\nDraft:\n{state['draft']}")
    else:
        prompt = (f"Write a short weekly newsletter for Café Comet, a neighbourhood café, about: {state['topic']}\n"
                  f"{FACTS}\nUse only these facts.")
    draft = writer_model.invoke(prompt).content
    print(f"\n✍️  Writer, round {state['rounds'] + 1}: {len(draft.split())} words")
    return {"draft": draft, "rounds": state["rounds"] + 1}


def edit(state: Studio):
    review = editor_model.with_structured_output(Review, method="json_schema").invoke(
        f"You are a strict editor.\n{EDITOR_RULES}\n\nThe facts:\n{FACTS}\n\nNewsletter to review:\n{state['draft']}"
    )
    print(f"🧐 Editor: {'approved ✅' if review.approved else 'changes needed: ' + review.feedback}")
    return {"approved": review.approved, "feedback": review.feedback}


def next_step(state: Studio):
    if state["approved"] or state["rounds"] >= MAX_ROUNDS:
        return "done"
    return "rewrite"


graph = StateGraph(Studio)
graph.add_node("write", write)
graph.add_node("edit", edit)
graph.add_edge(START, "write")
graph.add_edge("write", "edit")
graph.add_conditional_edges("edit", next_step, {"rewrite": "write", "done": END})
studio = graph.compile()

topic = input("Newsletter topic (for example: our new autumn menu): ")
result = studio.invoke({"topic": topic, "draft": "", "feedback": "", "approved": False, "rounds": 0})
print("\n" + "=" * 60 + f"\nFinal newsletter (after {result['rounds']} round(s)):\n\n{result['draft']}")
