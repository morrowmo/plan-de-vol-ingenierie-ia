# Chapitre 10 : trier les mêmes avis avec de petits modèles gratuits qui tournent
# sur VOTRE ordinateur.
import csv
from pathlib import Path

from transformers import pipeline

DATA = Path(__file__).parent.parent / "data"

with open(DATA / "reviews.csv", encoding="utf-8") as file:
    reviews = [row["review"] for row in csv.DictReader(file)]

# 1. Un modèle de la famille BERT entraîné uniquement à l’analyse de sentiment :
#    un couteau à pain, une seule tâche, bien faite.
#    Il ne connaît que deux étiquettes : POSITIVE et NEGATIVE.
sentiment = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

# 2. La classification zero-shot utilise un modèle NLI : il teste « This example is {label}. »
#    pour chaque étiquette que vous inventez, et choisit la plus probable. Aucun entraînement !
zero_shot = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
labels = ["positive", "negative", "neutral"]

# Bonus : le même détective peut trier par SUJET, avec des étiquettes inventées à l’instant.
topics = ["food and drinks", "service and staff", "prices", "place and comfort"]

print(f"{'BERT':<9} | {'zero-shot':<9} | {'topic':<17} | review")
for review in reviews:
    bert_label = sentiment(review)[0]["label"].lower()
    zs_label = zero_shot(review, candidate_labels=labels)["labels"][0]
    topic = zero_shot(review, candidate_labels=topics)["labels"][0]
    print(f"{bert_label:<9} | {zs_label:<9} | {topic:<17} | {review}")
