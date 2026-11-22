# Chapitre 17 : brancher le serveur MCP sur un agent.
import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()
SERVER_FILE = Path(__file__).parent / "cafe_menu_server.py"


async def main():
    # 1. Décrire comment joindre chaque serveur MCP. Le nôtre est un fichier Python lancé
    # sur le moment.
    client = MultiServerMCPClient({
        "cafe_menu": {"transport": "stdio", "command": sys.executable, "args": [str(SERVER_FILE)]},
    })
    tools = await client.get_tools()  # 2. Demander au serveur quels outils il propose
    print("Tools found on the MCP server:", [t.name for t in tools])

    # 3. Confier ces outils à un agent, exactement comme nos propres outils Python
    agent = create_agent(model="groq:openai/gpt-oss-120b", tools=tools,
                         system_prompt="You are Nova, the assistant of Café Comet.")
    result = await agent.ainvoke({"messages": [{"role": "user",
                                  "content": "What's Thursday's special, and how much does it cost?"}]})
    print("Nova:", result["messages"][-1].content)


asyncio.run(main())  # les outils MCP sont « async » : ils attendent le serveur sans tout bloquer
