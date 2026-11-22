# Chapitre 11 : transformer des phrases en coordonnées GPS du sens (embeddings).
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

sentences = [
    "I'd love a hot drink.",
    "Could I get a warm beverage?",
    "Where can I park my car?",
]
embeddings = model.encode(sentences)  # une liste de nombres par phrase

print(f"Each sentence became {len(embeddings[0])} numbers.")
print("The first 5 numbers of sentence 1:", embeddings[0][:5].round(3))

# Similarité cosinus : deux flèches pointent-elles dans la même direction ?
# 1 = même sens, 0 = aucun rapport.
scores = model.similarity(embeddings, embeddings)
print(f"\nhot drink  vs warm beverage: {scores[0][1]:.2f}")
print(f"hot drink  vs parking      : {scores[0][2]:.2f}")
