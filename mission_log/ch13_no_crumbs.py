# Journal de bord, chapitre 13 : arrêter de découper dès que la fin de la page est atteinte,
# pour ne pas fabriquer de minuscules fiches « miettes » faites de mots déjà présents
# dans la fiche précédente.
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"

CHUNK_SIZE = 40
OVERLAP = 10


def chunk_text(text):
    """Découpe un texte en fragments qui se chevauchent, sans dernière miette inutile."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunk = " ".join(words[start:start + CHUNK_SIZE])
        chunks.append(chunk)
        if start + CHUNK_SIZE >= len(words):  # cette fiche atteint déjà le dernier mot
            break
        start = start + CHUNK_SIZE - OVERLAP
    return chunks


count = 0
for file in sorted((DATA / "handbook").glob("*.md")):
    chunks = chunk_text(file.read_text(encoding="utf-8"))
    count = count + len(chunks)
    print(f"{file.name}: {len(chunks)} cards, the last one has {len(chunks[-1].split())} words")
print(f"\n{count} cards in total.")
