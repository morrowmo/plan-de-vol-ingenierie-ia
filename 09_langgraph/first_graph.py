# Chapitre 22 : un premier plan LangGraph, sans aucune IA, pour bien voir les pièces.
# Une commande de boisson voyage de station en station (les nœuds) le long des lignes
# (les arêtes).
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


# Le ticket que porte chaque voyageur : l’état
class DrinkOrder(TypedDict):
    drink: str
    temperature: str
    steps: list[str]


# Les stations : chacune lit le ticket et renvoie ce qu’elle modifie
def take_order(state: DrinkOrder):
    temperature = "cold" if "iced" in state["drink"].lower() else "hot"
    return {"temperature": temperature, "steps": state["steps"] + ["order taken"]}


def heat_milk(state: DrinkOrder):
    return {"steps": state["steps"] + ["milk heated"]}


def add_ice(state: DrinkOrder):
    return {"steps": state["steps"] + ["ice added"]}


def serve(state: DrinkOrder):
    return {"steps": state["steps"] + [f"{state['drink']} served"]}


# Le carrefour : décider quelle ligne prendre ensuite
def hot_or_cold(state: DrinkOrder):
    return "add_ice" if state["temperature"] == "cold" else "heat_milk"


# Dessiner le plan
graph = StateGraph(DrinkOrder)
graph.add_node("take_order", take_order)
graph.add_node("heat_milk", heat_milk)
graph.add_node("add_ice", add_ice)
graph.add_node("serve", serve)

graph.add_edge(START, "take_order")
graph.add_conditional_edges("take_order", hot_or_cold, ["heat_milk", "add_ice"])
graph.add_edge("heat_milk", "serve")
graph.add_edge("add_ice", "serve")
graph.add_edge("serve", END)

app = graph.compile()

for drink in ["Cappuccino", "Iced Latte"]:
    result = app.invoke({"drink": drink, "temperature": "", "steps": []})
    print(f"{drink}: {' -> '.join(result['steps'])}")

print("\nThe map, as Mermaid code (paste it into mermaid.live to see it drawn):")
print(app.get_graph().draw_mermaid())
