# Chapitre 16, approche 2 : « le kit repas ». create_agent écrit la boucle pour nous.
from dotenv import load_dotenv
from langchain.agents import create_agent

from cafe_tools import get_menu, get_weather

load_dotenv()

agent = create_agent(
    model="groq:openai/gpt-oss-120b",
    tools=[get_weather, get_menu],
    system_prompt=(
        "You are Nova, the assistant of Café Comet in Lyon. "
        "Use your tools to check facts. Suggest menu items that suit the weather. "
        "Only suggest items that are on the menu, at their exact menu price. "
        "Reply in plain text, no tables, in at most four sentences."
    ),
)

question = "What's the weather like in Lyon today, and what should we put on the specials board?"
result = agent.invoke({"messages": [{"role": "user", "content": question}]})

# L’agent renvoie tous les messages de son travail : question, appels d’outils,
# résultats des outils, réponse.
for message in result["messages"]:
    if message.type == "ai" and message.tool_calls:
        print(f"   [Nova uses: {', '.join(c['name'] for c in message.tool_calls)}]")
print("Nova:", result["messages"][-1].content)
