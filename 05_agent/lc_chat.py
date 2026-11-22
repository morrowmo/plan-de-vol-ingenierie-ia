# Chapitre 15 : la conversation de la Planète Chatbot, refaite avec le wrapper LangChain.
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage, SystemMessage

load_dotenv()  # LangChain trouve tout seul GROQ_API_KEY dans l’environnement

# « fournisseur:modèle » : l’adaptateur de prise universel.
# Changez cette seule chaîne pour changer de fournisseur.
model = init_chat_model("groq:openai/gpt-oss-120b", temperature=0.7)

history = [SystemMessage("You are Nova, the friendly assistant of Café Comet. Answer in two sentences at most.")]

print("Nova (LangChain edition) is ready. Type 'bye' to leave.")
while True:
    user_message = input("You: ")
    if user_message.lower() in ["bye", "quit", "exit"]:
        break
    history.append(HumanMessage(user_message))
    reply = model.invoke(history)  # même idée que client.chat.completions.create(...)
    history.append(AIMessage(reply.content))
    print("Nova:", reply.content)
print("Nova: See you soon at Café Comet!")
