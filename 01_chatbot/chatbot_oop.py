# Chapitre 7 : Nova sous forme de classe (un appareil de cuisine avec des boutons),
# qui compte les tokens et le coût.
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Prix en dollars US par million de tokens. Vérifiez sur console.groq.com/docs/models :
# ils changent !
PRICE_INPUT_PER_MILLION = 0.15
PRICE_OUTPUT_PER_MILLION = 0.60


class Chatbot:
    def __init__(self, system_prompt, model="openai/gpt-oss-120b"):
        self.client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
        self.history = [{"role": "system", "content": system_prompt}]
        self.input_tokens = 0   # tokens ENVOYÉS, cumulés sur toute la conversation
        self.output_tokens = 0  # tokens REÇUS

    def chat(self, user_message):
        self.history.append({"role": "user", "content": user_message})
        response = self.client.chat.completions.create(
            model=self.model, messages=self.history, temperature=0.7, max_tokens=500,
            reasoning_effort="low",
        )
        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})

        # Le fournisseur nous dit combien de tokens cet appel a utilisés : le compteur du taxi.
        self.input_tokens += response.usage.prompt_tokens
        self.output_tokens += response.usage.completion_tokens
        return reply

    def total_tokens(self):
        return self.input_tokens + self.output_tokens

    def cost(self):
        """Renvoie le coût de la conversation jusqu’ici, en dollars."""
        return (
            self.input_tokens / 1_000_000 * PRICE_INPUT_PER_MILLION
            + self.output_tokens / 1_000_000 * PRICE_OUTPUT_PER_MILLION
        )


if __name__ == "__main__":
    nova = Chatbot("You are Nova, the friendly assistant of Café Comet. Answer in two sentences at most.")
    print("Nova is ready. Type 'bye' to leave.")
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["bye", "quit", "exit"]:
            break
        print("Nova:", nova.chat(user_message))
        print(f"   [tokens so far: {nova.total_tokens()} | cost so far: ${nova.cost():.6f}]")
    print("Nova: See you soon at Café Comet!")
