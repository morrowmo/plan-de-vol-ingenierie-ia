# Journal de bord, chapitre 3 : accepter « croissant », « CROISSANT »
# et « Croissant » de la même façon.
menu = {"Espresso": 2.20, "Croissant": 1.90, "Hot Chocolate": 3.80}
total = 0

print("Welcome to Café Comet! Type an item from the menu, or 'done' to pay.")
while True:
    item = input("Order: ").title()  # « hot chocolate » -> « Hot Chocolate »
    if item == "Done":               # .title() a transformé « done » en « Done »
        break
    if item in menu:
        total = total + menu[item]
        print(f"Added {item}. Total so far: {total:.2f} €")
    else:
        print("Sorry, that's not on the menu.")

print(f"Please pay {total:.2f} €. Thank you!")
