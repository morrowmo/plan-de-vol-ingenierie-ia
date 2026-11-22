# Chapitre 3 : le kit de survie Python
# Une toute petite calculatrice d’addition pour le Café Comet.

# 1. Les variables : des bocaux étiquetés qui contiennent chacun une valeur
cafe_name = "Café Comet"
tip_percent = 10

# 2. Un dictionnaire : l’ardoise du menu, où chaque nom de produit renvoie à son prix
menu = {
    "Espresso": 2.20,
    "Croissant": 1.90,
    "Hot Chocolate": 3.80,
}

# 3. Une liste : une liste de courses, dont les éléments restent dans l’ordre
order = ["Espresso", "Croissant", "Croissant"]


# 4. Une fonction : une fiche recette réutilisable
def add_tip(amount, percent):
    """Renvoie le montant, pourboire compris."""
    return amount + amount * percent / 100


# 5. Une boucle : répéter la même étape pour chaque produit de la commande
total = 0
for item in order:
    price = menu[item]
    print(f"{item:<15} {price:.2f} €")
    total = total + price

# 6. Une décision avec if / else
if total > 5:
    print("You get a free loyalty stamp!")
else:
    print("Spend more than 5 € to get a stamp.")

print(f"{'Total':<15} {total:.2f} €")
print(f"{'With tip':<15} {add_tip(total, tip_percent):.2f} €")


# 7. Une classe : un emporte-pièce qui fabrique des objets de la même forme
class Customer:
    def __init__(self, name):
        self.name = name      # chaque client garde son propre nom...
        self.stamps = 0       # ...et son propre nombre de tampons

    def add_stamp(self):
        self.stamps = self.stamps + 1
        print(f"{self.name} now has {self.stamps} stamp(s).")


marta = Customer("Marta")
marta.add_stamp()
marta.add_stamp()
print(f"Thank you for visiting {cafe_name}!")
