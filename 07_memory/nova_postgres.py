# Chapitre 20 : l’armoire ignifugée. La même Nova, mais ses souvenirs survivent
# à un redémarrage.
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:comet@localhost:5432/postgres")

# « with » ouvre la connexion à la base de données et la referme proprement à la fin.
with PostgresSaver.from_conn_string(POSTGRES_URL) as checkpointer:
    checkpointer.setup()  # crée les tables la première fois (sans risque à chaque lancement)

    agent = create_agent(
        model="groq:openai/gpt-oss-120b",
        system_prompt="You are Nova, the assistant of Café Comet. Be brief and remember what customers tell you.",
        checkpointer=checkpointer,
    )

    customer = input("Customer name: ")
    print("Type 'bye' to leave. Then run the program again: Nova will still remember you!")
    while True:
        user_message = input(f"{customer}: ")
        if user_message.lower() in ["bye", "quit", "exit"]:
            break
        config = {"configurable": {"thread_id": customer}}
        result = agent.invoke({"messages": [{"role": "user", "content": user_message}]}, config)
        print("Nova:", result["messages"][-1].content)
