# Chapitre 13 : construire la bibliothèque. Découper le manuel en fiches (fragments),
# donner à chaque fiche ses coordonnées de sens (embeddings) et les classer dans Chroma.
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

DATA = Path(__file__).parent.parent / "data"
DB_FOLDER = Path(__file__).parent / "chroma_db"  # où Chroma range son classeur sur le disque

CHUNK_SIZE = 40  # mots par fiche
OVERLAP = 10     # mots repris de la fiche précédente, pour ne couper aucune idée en deux


def chunk_text(text):
    """Découpe un texte en fragments de CHUNK_SIZE mots qui se chevauchent."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunk = " ".join(words[start:start + CHUNK_SIZE])
        chunks.append(chunk)
        start = start + CHUNK_SIZE - OVERLAP  # avancer, mais pas jusqu’au bout
    return chunks


# 1. Préparer la base de connaissances : lire chaque page du manuel et la découper en fiches.
ids, documents, metadatas = [], [], []
for file in sorted((DATA / "handbook").glob("*.md")):
    text = file.read_text(encoding="utf-8")
    for number, chunk in enumerate(chunk_text(text)):
        ids.append(f"{file.stem}-{number}")             # une cote, par ex. « 02-allergens-1 »
        documents.append(chunk)
        metadatas.append({"source": file.name})         # retenir de quelle page vient la fiche

print(f"Cut {len(set(m['source'] for m in metadatas))} pages into {len(documents)} cards.")
print("Example card:", ids[0], "->", documents[0][:80], "...")

# 2. Convertir chaque fiche en embeddings (ses coordonnées GPS du sens).
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(documents).tolist()

# 3. Classer les fiches dans la base de données vectorielle Chroma.
client = chromadb.PersistentClient(path=str(DB_FOLDER))
collection = client.get_or_create_collection(
    name="cafe_handbook",
    configuration={"hnsw": {"space": "cosine"}},  # comparer les flèches par direction (cosinus)
)
# upsert = « update or insert » (mettre à jour ou insérer) : grâce à nos ID stables,
# relancer ce script remplace les fiches au lieu de les classer en double.
collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
print(f"The filing cabinet now holds {collection.count()} cards.")
