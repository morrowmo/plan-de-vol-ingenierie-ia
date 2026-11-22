# Chapitre 7 : c’est quoi, un token ? Comptons les briques de Lego avec tiktoken.
import tiktoken

# o200k_harmony est la « règle graduée » de gpt-oss, le modèle que nous utilisons avec Groq.
encoding = tiktoken.get_encoding("o200k_harmony")

sentences = [
    "Hello!",
    "I would like a cappuccino, please.",
    "Je voudrais un cappuccino, s’il vous plaît.",
    "☕🥐🚀",
    "Supercalifragilisticexpialidocious",
]

for sentence in sentences:
    tokens = encoding.encode(sentence)               # texte -> liste de nombres
    pieces = [encoding.decode([t]) for t in tokens]  # chaque nombre redevient son morceau de texte
    print(f"{len(tokens):>2} tokens | {sentence}")
    print(f"           {pieces}")
