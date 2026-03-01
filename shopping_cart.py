import random

menu = {"pizza":80, "burger":50, "chips":20, "pepsi":50, "mystery_bevreage":50}
mystery_bevreage = {"dew", "monster", "fanta", "7up"}

total = 0  
cart_list = []

print("======|MENU|======")
for key, values in menu.items():
    print(f"{key:100}: ₹{values:.2f}")
    print("========================")

while True:
    food = input("SELECT THE ITEMS YOU WOULD LIKE FROM MENU(q to quit)")

    if food == "q":
        break
    elif menu.get(food) is not None:
        if food == "mystery_bevreage":
            actual_drink = random.choice(list(mystery_bevreage))
            print(f"🎲 Your mystery beverage is: {actual_drink}!")
            cart_list.append(food)
        else:
            cart_list.append(food)


print("========================")
for food in cart_list:
    price = menu.get(food)
    total += price
print(f"TOTAL AMOUNT: ₹{total:.2f}")