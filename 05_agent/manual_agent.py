# Chapitre 16, approche 1 : « la cuisine maison ». On écrit nous-mêmes la boucle de l’agent.
# Le LLM décide quel outil appeler ; c’est NOUS qui lançons l’outil et lui rendons le résultat.
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from cafe_tools import get_weather  # notre boîte à outils de cafe_tools.py

load_dotenv()
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"

# L’« étiquette » de l’outil, dans le format JSON que comprend le LLM.
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get today's weather forecast for a city.",
        "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]},
    },
}]

messages = [
    {"role": "system", "content": "You are Nova, the assistant of Café Comet in Lyon. Use tools when you need facts. Reply in plain text, no tables, in at most four sentences."},
    {"role": "user", "content": "Should we put the terrace chairs out today?"},
]

for step in range(5):  # ne jamais laisser un agent tourner sans fin : 5 étapes maximum
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:        # aucun outil nécessaire : c’est la réponse finale
        print("Nova:", message.content)
        break

    for call in message.tool_calls:   # le LLM a demandé un ou plusieurs outils
        arguments = json.loads(call.function.arguments)
        print(f"   [step {step + 1}: calling {call.function.name}({arguments})]")
        result = get_weather.invoke(arguments)
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
