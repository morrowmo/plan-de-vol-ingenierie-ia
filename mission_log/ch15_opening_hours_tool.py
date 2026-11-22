# Journal de bord, chapitre 15 : un troisième outil pour la boîte à outils de Nova,
# testé à la main (pas besoin de clé d’API).
from pathlib import Path

from langchain.tools import tool

DATA = Path(__file__).parent.parent / "data"


@tool
def get_opening_hours() -> str:
    """Get Café Comet's opening hours for every day of the week, including public holidays."""
    return (DATA / "handbook" / "01-opening-hours.md").read_text(encoding="utf-8")


print("Name:", get_opening_hours.name)
print("Description:", get_opening_hours.description)
print(get_opening_hours.invoke({}))
