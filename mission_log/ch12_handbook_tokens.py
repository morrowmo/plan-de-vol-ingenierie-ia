# Journal de bord, chapitre 12 : le manuel entier ou trois fiches ? On compte les tokens,
# puis le coût.
from pathlib import Path

import tiktoken

DATA = Path(__file__).parent.parent / "data"
encoding = tiktoken.get_encoding("o200k_harmony")  # la règle graduée de gpt-oss, vue au chapitre 7
PRICE_IN = 0.15 / 1_000_000                        # dollars par token en entrée

total = 0
for file in sorted((DATA / "handbook").glob("*.md")):
    tokens = len(encoding.encode(file.read_text(encoding="utf-8")))
    total = total + tokens
    print(f"{tokens:>4} tokens | {file.name}")

cards = 3 * 40 * 1.3  # trois fiches de 40 mots, environ 1,3 token par mot
print(f"\nWhole handbook: {total} tokens. Three cards: about {cards:.0f} tokens.")
print(f"1,000 questions with the whole handbook: ${total * 1000 * PRICE_IN:.4f}")
print(f"1,000 questions with three cards:        ${cards * 1000 * PRICE_IN:.4f}")
