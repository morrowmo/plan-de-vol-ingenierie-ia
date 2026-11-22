# Journal de bord, chapitre 25 : une limite stricte sur les remboursements, en Python,
# avant la question d’approbation.
# Les outils verts s’exécutent seuls. Les outils orange demandent d’abord à un humain.
# Les actions rouges ne sont jamais des outils.
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

sys.path.append(str(Path(__file__).parent.parent / "05_agent"))  # pour reprendre les outils de Nova
from cafe_tools import get_menu  # noqa: E402  (vert : lire le menu est sans danger)

load_dotenv()


@tool
def refund_customer(customer: str, amount_euros: float, reason: str) -> str:
    """Refund a customer. Use only when the manager asks for a refund."""
    if amount_euros > 10:  # une règle stricte : aucun prompt ne peut contourner un if
        return "Refunds above 10 € must be done by the manager at the till."
    # ORANGE : l’agent peut PROPOSER un remboursement, mais un humain doit dire oui.
    print(f"\n   [APPROVAL NEEDED] Refund {amount_euros:.2f} € to {customer} ({reason})")
    answer = input("   Type 'yes' to approve: ")
    if answer.strip().lower() != "yes":
        return "The manager did NOT approve this refund. Nothing was paid."
    return f"Refund of {amount_euros:.2f} € to {customer} recorded."  # ici, on appellerait la vraie caisse


# ROUGE : aucun outil ne permet de supprimer des avis ou de changer les prix.
# Ce que l’agent ne peut pas atteindre, il ne peut pas le casser.
agent = create_agent(
    model="groq:openai/gpt-oss-120b",
    tools=[get_menu, refund_customer],
    system_prompt=(
        "You are Nova, the assistant of Café Comet. You help the manager. "
        "Reply in plain text, in at most three sentences."
    ),
)

request = input("Manager: ")
result = agent.invoke({"messages": [{"role": "user", "content": request}]})
print("Nova:", result["messages"][-1].content)
