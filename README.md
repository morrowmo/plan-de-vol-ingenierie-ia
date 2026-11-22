# Plan de vol pour l’ingénierie IA : le code d’accompagnement

Tous les programmes du livre *Plan de vol pour l’ingénierie IA* (tome 3 de la série Les agents IA pour débutants), testés avec les versions exactes des bibliothèques indiquées dans `requirements.txt`.

Les programmes, les données du café et les réponses de Nova sont en anglais, la langue de travail du code dans le monde entier. Les commentaires du code sont en français. Rien ne vous empêche de parler français à Nova : essayez !

## Pour commencer (le chapitre 2 explique chaque étape)

1. **Installez Python 3.12** depuis [python.org](https://www.python.org/downloads/).
2. **Téléchargez ce dossier.**
3. **Créez votre environnement virtuel et installez les bibliothèques :**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows : .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Ajoutez vos clés.** Copiez `.env.example` sous le nom `.env`, puis collez-y votre clé Groq gratuite.
5. **Vérifiez votre installation :**
   ```bash
   python 00_boarding/hello_check.py
   ```

Lancez toujours les programmes depuis ce dossier, par exemple `python 01_chatbot/chat_v1.py`.

## Le voyage

| Dossier | Planète | Chapitres |
|---|---|---|
| `00_boarding` | Embarquement | 2–3 |
| `01_chatbot` | Planète Chatbot | 4–8 |
| `02_classifier` | Planète Classificateur | 9–10 |
| `03_embeddings` | Planète Embeddings | 11 |
| `04_rag` | Planète RAG : lancez `build_library.py` avant `ask_handbook.py` | 12–14 |
| `05_agent` | Planète Agent | 15–17 |
| `06_structured` | Planète Sortie structurée | 18–19 |
| `07_memory` | Planète Mémoire (PostgreSQL nécessaire pour les fichiers `postgres`) | 20 |
| `08_middleware` | Planète Middleware | 21 |
| `09_langgraph` | Planète LangGraph | 22–23 |
| `10_multi_agent` | Planète Multi-agent : lancez d’abord `04_rag/build_library.py` | 24 |
| `data` | Le menu, les avis, le manuel et les e-mails de commande du Café Comet | – |

## PostgreSQL en une ligne (Planète Mémoire)

Si vous avez Docker, lancez cette commande ; sinon, le chapitre 20 présente Postgres.app (Mac) et les installateurs Windows.

```bash
docker run -d --name comet-postgres -e POSTGRES_PASSWORD=comet -p 5432:5432 postgres:16
```

## Tout tester

```bash
./run_all.sh
```

Ce script lance chaque programme avec des réponses déjà tapées. Les programmes qui ont besoin d’une clé ou d’une base de données absente sont sautés.

## Les limites de l’offre gratuite (Groq, vérifiées en 2026-11)

Le livre utilise `openai/gpt-oss-120b`, qui coûte 0,15 $ par million de tokens en entrée et 0,60 $ par million de tokens en sortie. L’offre gratuite a deux limites :

- **8 000 tokens par minute.** Si vous atteignez cette limite, attendez quelques secondes et relancez le programme.
- **200 000 tokens par jour.** C’est largement assez pour une planète par jour. Lancer tous les programmes d’affilée (`run_all.sh`) en consomme la plus grande partie.

Si Groq retire ce modèle, remplacez `openai/gpt-oss-120b` par un modèle actuel de [console.groq.com/docs/models](https://console.groq.com/docs/models).
