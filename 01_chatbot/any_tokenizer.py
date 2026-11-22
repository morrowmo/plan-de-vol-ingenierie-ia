# Chapitre 7 : chaque modèle mesure le texte avec sa propre règle graduée.
# AutoTokenizer télécharge seulement le tokenizer d’un modèle depuis Hugging Face
# (quelques Mo).
import tiktoken
from transformers import AutoTokenizer

text = "Je voudrais un cappuccino et deux croissants, s’il vous plaît."

print(f"tiktoken o200k_harmony: {len(tiktoken.get_encoding('o200k_harmony').encode(text))} tokens")

for model_name in ["openai/gpt-oss-120b", "Qwen/Qwen2.5-7B-Instruct", "google-bert/bert-base-uncased"]:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.encode(text, add_special_tokens=False)
    print(f"{model_name:<30}: {len(tokens)} tokens")
