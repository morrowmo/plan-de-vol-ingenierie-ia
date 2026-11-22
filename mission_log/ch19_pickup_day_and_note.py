# Journal de bord, chapitre 19 : une case pour le jour de retrait, et une note facultative
# sur le bon de commande.
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

load_dotenv()
DATA = Path(__file__).parent.parent / "data"


class OrderLine(BaseModel):
    item: str = Field(description="Name of the menu item, for example 'Croissant'")
    quantity: int = Field(description="How many of this item")


class Order(BaseModel):
    customer_name: str = Field(description="First name of the customer, or 'unknown'")
    items: list[OrderLine] = Field(description="Every item ordered")
    pickup_day: str = Field(description="The day of pickup as written in the email, for example 'tomorrow' or 'Friday'")
    pickup_time: str = Field(description="When the customer will come, as written in the email")
    # Case facultative : du texte, ou rien du tout. Elle reste vide (None) si l’e-mail
    # n’en mentionne pas.
    note: str | None = Field(default=None, description="Any special request or occasion, if the email mentions one")


model = init_chat_model("groq:openai/gpt-oss-120b", temperature=0)
form_filler = model.with_structured_output(Order, method="json_schema")

emails = (DATA / "order_emails.txt").read_text(encoding="utf-8").split("---")
for email in emails:
    order = form_filler.invoke(f"Extract the order from this customer email:\n{email.strip()}")
    print(f"\n📧 {email.strip()[:60]}...")
    print(f"   Customer: {order.customer_name} | Pickup: {order.pickup_day}, {order.pickup_time}")
    for line in order.items:
        print(f"   - {line.quantity} x {line.item}")
    if order.note:  # None (une case vide) compte comme faux
        print(f"   Note: {order.note}")
