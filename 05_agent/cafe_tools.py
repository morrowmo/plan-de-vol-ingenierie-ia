# Planète Agent : les outils de la boîte à outils de Nova. Ce sont de simples fonctions Python.
# L’étiquette @tool transforme une fonction en outil ; la docstring dit au LLM à quoi il sert.
import json
import re
from pathlib import Path

import requests
from ddgs import DDGS
from langchain.tools import tool

DATA = Path(__file__).parent.parent / "data"


@tool
def get_weather(city: str) -> str:
    """Get today's weather forecast for a city (temperature in °C and rain)."""
    # 1. Trouver les coordonnées de la ville (service gratuit Open-Meteo, sans clé)
    place = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search", params={"name": city, "count": 1}, timeout=10
    ).json()
    if not place.get("results"):
        return f"I couldn't find a city called {city}."
    lat, lon = place["results"][0]["latitude"], place["results"][0]["longitude"]
    # 2. Demander la météo du jour à ces coordonnées
    forecast = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "timezone": "auto", "forecast_days": 1,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max"},
        timeout=10,
    ).json()["daily"]
    return (f"{city} today: between {forecast['temperature_2m_min'][0]}°C and "
            f"{forecast['temperature_2m_max'][0]}°C, {forecast['precipitation_probability_max'][0]}% chance of rain.")


@tool
def get_menu() -> str:
    """Get Café Comet's full menu with prices in euros."""
    menu = json.loads((DATA / "menu.json").read_text(encoding="utf-8"))
    return "\n".join(f"{item['name']}: {item['price']:.2f} € - {item['description']}" for item in menu)


@tool
def web_search(query: str) -> str:
    """Search the web. Returns the titles, links and snippets of the top 3 results."""
    try:
        results = DDGS().text(query, max_results=3)
    except Exception as error:  # un outil doit signaler les problèmes, jamais faire planter l’agent
        return f"The search failed ({error}). Try different words."
    return "\n\n".join(f"{r['title']}\n{r['href']}\n{r['body']}" for r in results)


@tool
def read_web_page(url: str) -> str:
    """Read the text of a web page (the first 1,500 characters), given its full URL."""
    try:
        html = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}).text
    except Exception as error:
        return f"Could not open the page ({error})."
    html = re.sub(r"<(script|style).*?</\1>", " ", html, flags=re.DOTALL)  # retirer code et styles
    text = re.sub(r"<[^>]+>", " ", html)                                   # retirer les balises
    text = re.sub(r"\s+", " ", text)                                       # ranger les espaces
    return text[:1500]  # rester court : chaque caractère envoyé coûte des tokens
