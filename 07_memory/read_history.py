# Chapitre 20 : ouvrir l’armoire et relire d’anciennes conversations.
import os

import psycopg
from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:comet@localhost:5432/postgres")

# 1. Du SQL tout simple : quels carnets (fils) existent dans la base de données ?
with psycopg.connect(POSTGRES_URL) as connection:
    rows = connection.execute("SELECT DISTINCT thread_id FROM checkpoints ORDER BY thread_id").fetchall()
threads = [row[0] for row in rows]
print("Customers in the database:", threads)

# 2. Le checkpointer lit pour nous le dernier point de sauvegarde d’un fil.
customer = input("Whose conversation do you want to read? ")
with PostgresSaver.from_conn_string(POSTGRES_URL) as checkpointer:
    saved = checkpointer.get_tuple({"configurable": {"thread_id": customer}})
    if saved is None:
        print("No conversation found for", customer)
    else:
        for message in saved.checkpoint["channel_values"]["messages"]:
            print(f"{message.type:>6}: {message.content}")
