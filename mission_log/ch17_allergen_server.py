# Journal de bord, chapitre 17 : le serveur MCP du Café Comet, avec un troisième outil
# pour les allergènes.
# Ne lancez pas ce fichier vous-même : ch17_allergen_agent.py s’en charge.
import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

DATA = Path(__file__).parent.parent / "data"
server = FastMCP("cafe-comet-menu", log_level="WARNING")  # n’afficher que les vrais problèmes


@server.tool()
def list_menu() -> str:
    """List every item on Café Comet's menu with its price in euros."""
    menu = json.loads((DATA / "menu.json").read_text(encoding="utf-8"))
    return "\n".join(f"{item['name']}: {item['price']:.2f} €" for item in menu)


@server.tool()
def daily_special(day: str) -> str:
    """Return the special of the day for a day of the week (for example 'Monday')."""
    specials = {"monday": "Tomato Soup", "tuesday": "Avocado Toast", "wednesday": "Chai Latte",
                "thursday": "Comet Cheesecake", "friday": "Hot Chocolate",
                "saturday": "Vegan Banana Bread", "sunday": "Croissant"}
    return specials.get(day.lower(), "No special for that day.")


@server.tool()
def allergen_info() -> str:
    """Get Café Comet's allergen and special-diet rules. Use it for ANY question about allergies,
    nuts, gluten, eggs, milk or vegan food."""
    return (DATA / "handbook" / "02-allergens.md").read_text(encoding="utf-8")


if __name__ == "__main__":
    server.run(transport="stdio")  # dialoguer par le « câble » de l’entrée/sortie standard
