# Chapitre 10 : l’inférence en langage naturel (NLI). Les trois verdicts du détective.
# L’hypothèse DÉCOULE-t-elle de la prémisse (entailment), la CONTREDIT-elle,
# ou ni l’un ni l’autre (neutral) ?
from transformers import pipeline

detective = pipeline("text-classification", model="cross-encoder/nli-deberta-v3-base")

premise = "The café opens at 7:30 on weekdays and is closed on public holidays."
hypotheses = [
    "The café is open on weekdays.",         # découle de la prémisse
    "The café is open on public holidays.",  # dit le contraire
    "The café sells good croissants.",       # la prémisse n’en dit rien

]

for hypothesis in hypotheses:
    result = detective({"text": premise, "text_pair": hypothesis})
    print(f"{result['label']:<14} ({result['score']:.0%}) | {hypothesis}")
