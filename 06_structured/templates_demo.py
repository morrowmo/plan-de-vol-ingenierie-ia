# Chapitre 18 : les prompts dynamiques. Des lettres à trous pour le LLM.
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

load_dotenv()
model = init_chat_model("groq:openai/gpt-oss-120b", temperature=0.7)

# 1. PromptTemplate : un texte avec des trous entre {accolades}
welcome = PromptTemplate.from_template(
    "Write a one-sentence welcome message for {name}, who loves {favourite}."
)
prompt = welcome.invoke({"name": "Marta", "favourite": "cappuccino"})
print("Filled-in prompt:", prompt.text)
print("Nova:", model.invoke(prompt).content, "\n")

# 2. ChatPromptTemplate : un script à plusieurs rôles, chacun avec ses trous
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are Nova, the assistant of {cafe}. Answer in {language}, in one sentence."),
    ("user", "{question}"),
])
messages = chat_template.invoke({"cafe": "Café Comet", "language": "Spanish", "question": "Do you have oat milk?"})
print("Nova:", model.invoke(messages).content, "\n")

# 3. MessagesPlaceholder : une place réservée où viendra s’asseoir toute une conversation
memory_template = ChatPromptTemplate.from_messages([
    ("system", "You are Nova, the assistant of Café Comet. Be brief."),
    MessagesPlaceholder("history"),  # la place réservée
    ("user", "{question}"),
])
history = [
    ("user", "Hi, I'm Jules and I love chocolate, but I don't drink coffee."),
    ("assistant", "Nice to meet you, Jules! I'll keep that in mind."),
]
messages = memory_template.invoke({"history": history, "question": "What drink would you recommend for me?"})
print("Nova:", model.invoke(messages).content)
