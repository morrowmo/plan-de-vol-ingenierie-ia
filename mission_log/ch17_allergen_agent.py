# Journal de bord, chapitre 17 : brancher sur un agent le serveur doté de l’outil allergènes.
import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()
SERVER_FILE = Path(__file__).parent / "ch17_allergen_server.py"


async def main():
    client = MultiServerMCPClient({
        "cafe_menu": {"transport": "stdio", "command": sys.executable, "args": [str(SERVER_FILE)]},
    })
    tools = await client.get_tools()  # le nouvel outil apparaît tout seul : rien d’autre à changer
    print("Tools found on the MCP server:", [t.name for t in tools])

    agent = create_agent(model="groq:openai/gpt-oss-120b", tools=tools,
                         system_prompt="You are Nova, the assistant of Café Comet.")
    result = await agent.ainvoke({"messages": [{"role": "user",
                                  "content": "Can a customer with a nut allergy eat the Gluten-Free Brownie?"}]})
    print("Nova:", result["messages"][-1].content)


asyncio.run(main())
