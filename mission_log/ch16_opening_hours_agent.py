# Journal de bord, chapitre 16 : donner à l’agent météo un troisième outil,
# les horaires d’ouverture.
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

# Ce fichier se trouve dans mission_log : on indique donc à Python où trouver cafe_tools.py.
# (Si vous avez plutôt collé l’outil dans cafe_tools.py, cette ligne est inutile.)
sys.path.append(str(Path(__file__).parent.parent / "05_agent"))
from cafe_tools import get_menu, get_weather  # noqa: E402

load_dotenv()
DATA = Path(__file__).parent.parent / "data"


@tool
def get_opening_hours() -> str:
    """Get Café Comet's opening hours for every day of the week, including public holidays."""
    return (DATA / "handbook" / "01-opening-hours.md").read_text(encoding="utf-8")


agent = create_agent(
    model="groq:openai/gpt-oss-120b",
    tools=[get_weather, get_menu, get_opening_hours],
    system_prompt=(
        "You are Nova, the assistant of Café Comet in Lyon. "
        "Use your tools to check facts: the weather, the menu and the opening hours. "
        "Only suggest items that are on the menu, at their exact menu price. "
        "Reply in plain text, no tables, in at most four sentences."
    ),
)

question = "Is the café open on Sunday afternoon, and is it terrace weather in Lyon today?"
result = agent.invoke({"messages": [{"role": "user", "content": question}]})

for message in result["messages"]:
    if message.type == "ai" and message.tool_calls:
        print(f"   [Nova uses: {', '.join(c['name'] for c in message.tool_calls)}]")
print("Nova:", result["messages"][-1].content)
