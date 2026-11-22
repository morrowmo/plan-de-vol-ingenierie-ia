# Journal de bord, chapitre 10 : ajouter une étiquette de sujet, et compter les désaccords
# entre BERT et le zero-shot.
import csv
from pathlib import Path

from transformers import pipeline

DATA = Path(__file__).parent.parent / "data"

with open(DATA / "reviews.csv", encoding="utf-8") as file:
    reviews = [row["review"] for row in csv.DictReader(file)]

sentiment = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
zero_shot = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0")

# 1. Un cinquième sujet, inventé sur le moment : aucun entraînement nécessaire.
topics = ["food and drinks", "service and staff", "prices", "place and comfort", "noise and atmosphere"]

# 2. Compter les désaccords entre les deux trieurs de sentiment.
disagreements = 0
for review in reviews:
    bert_label = sentiment(review)[0]["label"].lower()
    zs_label = zero_shot(review, candidate_labels=["positive", "negative", "neutral"])["labels"][0]
    topic = zero_shot(review, candidate_labels=topics)["labels"][0]
    if bert_label != zs_label:
        disagreements += 1
    print(f"{topic:<20} | {review}")

print(f"\nBERT and zero-shot disagree on {disagreements} of {len(reviews)} reviews.")
