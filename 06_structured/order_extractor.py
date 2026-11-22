# Chapitre 19 : la sortie structurée. Des e-mails de commande en vrac deviennent
# des bons de commande bien nets.
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

load_dotenv()
DATA = Path(__file__).parent.parent / "data"


# Le formulaire : chaque champ est une case vide, avec une note qui dit au LLM quoi y écrire.
class OrderLine(BaseModel):
    item: str = Field(description="Name of the menu item, for example 'Croissant'")
    quantity: int = Field(description="How many of this item")


class Order(BaseModel):
    customer_name: str = Field(description="First name of the customer, or 'unknown'")
    items: list[OrderLine] = Field(description="Every item ordered")
    pickup_time: str = Field(description="When the customer will come, as written in the email")


model = init_chat_model("groq:openai/gpt-oss-120b", temperature=0)
form_filler = model.with_structured_output(Order, method="json_schema")  # « remplis CE formulaire »

emails = (DATA / "order_emails.txt").read_text(encoding="utf-8").split("---")
for email in emails:
    order = form_filler.invoke(f"Extract the order from this customer email:\n{email.strip()}")
    print(f"\n📧 {email.strip()[:60]}...")
    print(f"   Customer: {order.customer_name} | Pickup: {order.pickup_time}")
    for line in order.items:
        print(f"   - {line.quantity} x {line.item}")
