# Chapitre 20 : des points de sauvegarde avec InMemorySaver, et un carnet par client
# (thread_id).
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

agent = create_agent(
    model="groq:openai/gpt-oss-120b",
    system_prompt="You are Nova, the assistant of Café Comet. Be brief and remember what customers tell you.",
    checkpointer=InMemorySaver(),  # le post-it : garde chaque étape, oublié à l’arrêt du programme
)

customer = input("Customer name: ")
print("Type 'switch' to serve another customer, 'bye' to leave.")
while True:
    user_message = input(f"{customer}: ")
    if user_message.lower() in ["bye", "quit", "exit"]:
        break
    if user_message.lower() == "switch":
        customer = input("Customer name: ")  # un autre nom ouvre un autre carnet
        continue

    config = {"configurable": {"thread_id": customer}}  # quel carnet utiliser
    result = agent.invoke({"messages": [{"role": "user", "content": user_message}]}, config)
    print("Nova:", result["messages"][-1].content)
