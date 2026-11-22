# Journal de bord, chapitre 22 : une troisième ligne sur la carte, pour les thés,
# avec un carrefour à trois routes.
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class DrinkOrder(TypedDict):
    drink: str
    temperature: str
    steps: list[str]


def take_order(state: DrinkOrder):
    temperature = "cold" if "iced" in state["drink"].lower() else "hot"
    return {"temperature": temperature, "steps": state["steps"] + ["order taken"]}


def heat_milk(state: DrinkOrder):
    return {"steps": state["steps"] + ["milk heated"]}


def add_ice(state: DrinkOrder):
    return {"steps": state["steps"] + ["ice added"]}


# La nouvelle station : les thés ont besoin d’eau chaude, pas de lait
def steep_tea(state: DrinkOrder):
    return {"steps": state["steps"] + ["tea steeped"]}


def serve(state: DrinkOrder):
    return {"steps": state["steps"] + [f"{state['drink']} served"]}


# Le carrefour a maintenant trois routes. Le test du thé passe en premier.
def which_line(state: DrinkOrder):
    if "tea" in state["drink"].lower():
        return "steep_tea"
    if state["temperature"] == "cold":
        return "add_ice"
    return "heat_milk"


graph = StateGraph(DrinkOrder)
graph.add_node("take_order", take_order)
graph.add_node("heat_milk", heat_milk)
graph.add_node("add_ice", add_ice)
graph.add_node("steep_tea", steep_tea)
graph.add_node("serve", serve)

graph.add_edge(START, "take_order")
graph.add_conditional_edges("take_order", which_line, ["heat_milk", "add_ice", "steep_tea"])
graph.add_edge("heat_milk", "serve")
graph.add_edge("add_ice", "serve")
graph.add_edge("steep_tea", "serve")
graph.add_edge("serve", END)

app = graph.compile()

for drink in ["Cappuccino", "Iced Latte", "Peppermint Tea"]:
    result = app.invoke({"drink": drink, "temperature": "", "steps": []})
    print(f"{drink}: {' -> '.join(result['steps'])}")
