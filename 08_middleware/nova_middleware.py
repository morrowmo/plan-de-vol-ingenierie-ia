# Chapitre 21 : les middlewares sont des contrôles de sécurité entre les étapes d’un agent.
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, before_model
from langchain_core.messages.utils import count_tokens_approximately
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


# 1. Notre propre petit contrôle : il s’exécute AVANT chaque appel au modèle
# et se contente de faire un rapport.
@before_model
def show_luggage(state, runtime):
    messages = state["messages"]
    print(f"   [checkpoint: {len(messages)} messages, about {count_tokens_approximately(messages)} tokens]")
    if "summary of the conversation" in str(messages[0].content):
        print("   [checkpoint: the oldest messages have been replaced by a summary]")
    return None  # None = « laisser passer le voyageur sans rien changer »


# 2. Un contrôle tout prêt : quand l’historique devient trop long, il rédige le compte rendu.
summariser = SummarizationMiddleware(
    model="groq:openai/gpt-oss-120b",
    trigger=("tokens", 300),  # résumer au-delà de ~300 tokens (minuscule, pour le voir en action)
    keep=("messages", 4),     # toujours garder mot pour mot les 4 messages les plus récents
)

agent = create_agent(
    model="groq:openai/gpt-oss-120b",
    system_prompt="You are Nova, the assistant of Café Comet. Answer in two or three sentences.",
    middleware=[show_luggage, summariser],  # l’ordre des contrôles compte
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "demo"}}
print("Chat with Nova for a while and watch the message count drop. Type 'bye' to leave.")
while True:
    user_message = input("You: ")
    if user_message.lower() in ["bye", "quit", "exit"]:
        break
    result = agent.invoke({"messages": [{"role": "user", "content": user_message}]}, config)
    print("Nova:", result["messages"][-1].content)
