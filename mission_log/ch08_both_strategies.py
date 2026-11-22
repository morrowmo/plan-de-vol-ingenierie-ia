# Journal de bord, chapitre 8 : une troisième stratégie, « both » : résumer d’abord,
# puis faire glisser si c’est encore trop long.
import os

import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PRICE_INPUT_PER_MILLION = 0.15
PRICE_OUTPUT_PER_MILLION = 0.60

# La taille de notre « tableau blanc » pour jouer. Les vrais modèles acceptent bien plus
# (souvent 128 000 tokens),
# mais un petit nombre permet de voir la fenêtre glisser au bout de quelques messages.
MAX_HISTORY_TOKENS = 300

# o200k_harmony est la règle graduée de gpt-oss : on compte exactement AVANT d’envoyer.
encoding = tiktoken.get_encoding("o200k_harmony")


def count_tokens(messages):
    return sum(len(encoding.encode(m["content"])) for m in messages)


class Chatbot:
    def __init__(self, system_prompt, model="openai/gpt-oss-120b", strategy="summary"):
        self.client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
        self.strategy = strategy  # « window » (effacer le début) ou « summary » (compte rendu)
        self.system_message = {"role": "system", "content": system_prompt}
        self.history = []         # la conversation, SANS le message système
        self.input_tokens = 0
        self.output_tokens = 0

    # ---------- garder le tableau blanc léger ----------
    def sliding_window(self):
        """Efface les plus vieux messages jusqu’à ce que l’historique tienne sur le tableau."""
        while count_tokens(self.history) > MAX_HISTORY_TOKENS and len(self.history) > 2:
            removed = self.history.pop(0)
            print(f"   [window: forgot an old {removed['role']} message]")

    def summarise_history(self):
        """Remplace la plus vieille moitié de l’historique par un court résumé (compte rendu)."""
        if count_tokens(self.history) <= MAX_HISTORY_TOKENS:
            return
        half = len(self.history) // 2
        old, recent = self.history[:half], self.history[half:]
        transcript = "\n".join(f"{m['role']}: {m['content']}" for m in old)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Summarise this conversation in 3 short bullet points. Keep names, orders and facts."},
                {"role": "user", "content": transcript},
            ],
            temperature=0,
            max_tokens=400,
            reasoning_effort="low",
        )
        self.add_usage(response.usage)
        summary = response.choices[0].message.content
        self.history = [{"role": "user", "content": f"(Summary of our earlier conversation)\n{summary}"},
                        {"role": "assistant", "content": "Thanks, I remember."}] + recent
        print("   [summary: old messages were replaced by a short summary]")

    # ---------- la conversation ----------
    def chat(self, user_message):
        self.history.append({"role": "user", "content": user_message})
        if self.strategy == "window":
            self.sliding_window()
        elif self.strategy == "both":
            self.summarise_history()
            self.sliding_window()
        else:
            self.summarise_history()

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[self.system_message] + self.history,  # le message système reste épinglé en haut
            temperature=0.7,
            max_tokens=500,
            reasoning_effort="low",
            stream=True,                                     # envoyer la réponse par morceaux
            stream_options={"include_usage": True},          # ...et le nombre de tokens à la fin
        )

        reply = ""
        print("Nova: ", end="", flush=True)
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                piece = chunk.choices[0].delta.content
                print(piece, end="", flush=True)  # afficher chaque morceau dès qu’il arrive
                reply += piece
            if chunk.usage:                       # le dernier morceau contient les totaux
                self.add_usage(chunk.usage)
        print()

        self.history.append({"role": "assistant", "content": reply})
        return reply

    def add_usage(self, usage):
        self.input_tokens += usage.prompt_tokens
        self.output_tokens += usage.completion_tokens

    def cost(self):
        return (self.input_tokens / 1_000_000 * PRICE_INPUT_PER_MILLION
                + self.output_tokens / 1_000_000 * PRICE_OUTPUT_PER_MILLION)


if __name__ == "__main__":
    nova = Chatbot("You are Nova, the friendly assistant of Café Comet. Answer in three sentences at most.", strategy="both")
    print("Nova is ready. Type 'bye' to leave.")
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["bye", "quit", "exit"]:
            break
        nova.chat(user_message)
        print(f"   [history: {count_tokens(nova.history)} tokens | cost so far: ${nova.cost():.6f}]")
    print("Nova: See you soon at Café Comet!")
