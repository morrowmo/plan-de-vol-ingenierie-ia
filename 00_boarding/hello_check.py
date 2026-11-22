# Chapitre 2 : vérifiez que votre valise est prête.
# Lancez-le avec :  python 00_boarding/hello_check.py
import os
import sys

from dotenv import load_dotenv

print(f"Python version: {sys.version.split()[0]}")
if sys.version_info < (3, 10):
    print("❌ Please install Python 3.10 or newer.")
else:
    print("✅ Python is recent enough.")

# Sommes-nous dans l’environnement virtuel (notre boîte à repas) ?
if sys.prefix != sys.base_prefix:
    print("✅ The virtual environment is active.")
else:
    print("❌ The virtual environment is NOT active. See chapter 2.")

# Charge les clés du fichier .env dans l’environnement
load_dotenv()
key = os.getenv("GROQ_API_KEY")
if key:
    # N’affichez jamais une clé entière ! Les 4 premiers caractères suffisent.
    print(f"✅ Groq key found (starts with {key[:4]}...).")
else:
    print("❌ No GROQ_API_KEY found. Check your .env file.")

# Cherche chaque bibliothèque sans la charger (certaines sont lentes à charger)
from importlib.util import find_spec

for library in ["openai", "langchain", "sentence_transformers", "chromadb"]:
    if find_spec(library):
        print(f"✅ {library} is installed.")
    else:
        print(f"❌ {library} is missing. Run: pip install -r requirements.txt")
