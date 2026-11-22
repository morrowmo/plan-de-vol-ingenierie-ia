# Chapitre 16, approche 3 : « la cuisine du restaurant ». On dessine l’agent
# sous forme de carte LangGraph.
# (Vous découvrirez chaque pièce sur la Planète LangGraph. Pour l’instant, lancez-le.)
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from cafe_tools import get_weather

load_dotenv()
model = init_chat_model("groq:openai/gpt-oss-120b").bind_tools([get_weather])


def call_model(state: MessagesState):
    return {"messages": [model.invoke(state["messages"])]}


graph = StateGraph(MessagesState)
graph.add_node("model", call_model)
graph.add_node("tools", ToolNode([get_weather]))
graph.add_edge(START, "model")
graph.add_conditional_edges("model", tools_condition, {"tools": "tools", END: END})  # un outil ? on y va
graph.add_edge("tools", "model")                                                       # puis retour au modèle
agent = graph.compile()

result = agent.invoke({"messages": [{"role": "user", "content": "Is it raining in Lyon today?"}]})
print("Nova:", result["messages"][-1].content)
