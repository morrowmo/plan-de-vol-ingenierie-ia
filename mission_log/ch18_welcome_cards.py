# Journal de bord, chapitre 18 : un seul modèle de bienvenue, rempli pour trois clients.
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

load_dotenv()
model = init_chat_model("groq:openai/gpt-oss-120b", temperature=0.7)

# La carte est écrite une fois pour toutes : sa formulation ne change jamais.
welcome = PromptTemplate.from_template(
    "Write a one-sentence welcome message for {name}, who loves {favourite}."
)

# Les prénoms comme clés, les produits préférés comme valeurs.
customers = {"Marta": "Cappuccino", "Jules": "Hot Chocolate", "Priya": "Comet Cheesecake"}

for name, favourite in customers.items():
    prompt = welcome.invoke({"name": name, "favourite": favourite})
    print(f"{name}: {model.invoke(prompt).content}")
