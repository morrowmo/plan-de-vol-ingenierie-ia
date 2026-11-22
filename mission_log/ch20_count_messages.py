# Journal de bord, chapitre 20 : compter les messages dans le carnet de chaque client,
# puis en lire un.
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

with PostgresSaver.from_conn_string(POSTGRES_URL) as checkpointer:
    # 2. La vue d’ensemble : une ligne par client, avec la taille de son carnet.
    for name in threads:
        saved = checkpointer.get_tuple({"configurable": {"thread_id": name}})
        messages = saved.checkpoint["channel_values"]["messages"]
        print(f"{name}: {len(messages)} messages")

    # 3. Puis lire un carnet, comme dans read_history.py.
    customer = input("Whose conversation do you want to read? ")
    saved = checkpointer.get_tuple({"configurable": {"thread_id": customer}})
    if saved is None:
        print("No conversation found for", customer)
    else:
        for message in saved.checkpoint["channel_values"]["messages"]:
            print(f"{message.type:>6}: {message.content}")
