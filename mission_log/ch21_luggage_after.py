# Journal de bord, chapitre 21 : un second contrôle APRÈS le résumeur, pour voir
# les bagages rétrécir.
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, before_model
from langchain_core.messages.utils import count_tokens_approximately
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


# Contrôle 1 : AVANT la sécurité (le résumeur)
@before_model
def show_luggage(state, runtime):
    messages = state["messages"]
    print(f"   [before security: {len(messages)} messages, about {count_tokens_approximately(messages)} tokens]")
    return None


# Contrôle 2 : APRÈS la sécurité. Même travail, autre place dans la file.
@before_model
def show_luggage_after(state, runtime):
    messages = state["messages"]
    print(f"   [after security:  {len(messages)} messages, about {count_tokens_approximately(messages)} tokens]")
    return None


summariser = SummarizationMiddleware(
    model="groq:openai/gpt-oss-120b",
    trigger=("tokens", 300),
    keep=("messages", 4),
)

agent = create_agent(
    model="groq:openai/gpt-oss-120b",
    system_prompt="You are Nova, the assistant of Café Comet. Answer in two or three sentences.",
    middleware=[show_luggage, summariser, show_luggage_after],  # avant, sécurité, après
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "demo"}}
print("Chat with Nova and compare the luggage before and after security. Type 'bye' to leave.")
while True:
    user_message = input("You: ")
    if user_message.lower() in ["bye", "quit", "exit"]:
        break
    result = agent.invoke({"messages": [{"role": "user", "content": user_message}]}, config)
    print("Nova:", result["messages"][-1].content)
