import random
from collections import defaultdict

from flask import Flask, render_template, request, redirect, url_for, session, flash

# Reuse the same menu as your console program
menu = {"pizza": 80, "burger": 50, "chips": 20, "pepsi": 50, "mystery_bevreage": 50}
mystery_bevreage = {"dew", "monster", "fanta", "7up"}


def build_cart_items(cart_list):
    """Cart is a list of {"key": ..., "revealed": ... (optional)}. Group and build display."""
    if not cart_list:
        return [], 0

    # Support old format: cart was a dict {key: qty}. Convert to list once.
    if isinstance(cart_list, dict):
        cart_list = [
            {"key": k, "revealed": random.choice(list(mystery_bevreage)) if k == "mystery_bevreage" else None}
            for k, qty in cart_list.items()
            for _ in range(qty)
        ]

    groups = defaultdict(int)  # (key, revealed_or_None) -> count
    for entry in cart_list:
        key = entry.get("key")
        revealed = entry.get("revealed")
        groups[(key, revealed)] += 1

    items = []
    total = 0
    for (key, revealed), qty in groups.items():
        price = menu.get(key, 0)
        subtotal = price * qty
        total += subtotal

        if key == "mystery_bevreage" and revealed:
            display_name = f"Mystery Beverage ({revealed})"
        elif key == "mystery_bevreage":
            display_name = "Mystery Beverage"
        else:
            display_name = key.capitalize()

        items.append(
            {
                "key": key,
                "name": display_name,
                "price": price,
                "quantity": qty,
                "subtotal": subtotal,
            }
        )

    return items, total


app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")
app.secret_key = "change-this-secret-key"


@app.route("/", methods=["GET"])
def index():
    cart = session.get("cart", [])

    # Migrate old dict cart to list format once (so drink names persist)
    if isinstance(cart, dict):
        cart = [
            {"key": k, "revealed": random.choice(list(mystery_bevreage)) if k == "mystery_bevreage" else None}
            for k, qty in cart.items()
            for _ in range(qty)
        ]
        session["cart"] = cart

    cart_items, total = build_cart_items(cart)
    return render_template("menu.html", menu=menu, cart_items=cart_items, total=total)


@app.route("/add", methods=["POST"])
def add_to_cart():
    item_key = request.form.get("item")

    if item_key in menu:
        cart = session.get("cart", [])

        # Support old session format: cart was a dict
        if isinstance(cart, dict):
            cart = [
                {"key": k, "revealed": random.choice(list(mystery_bevreage)) if k == "mystery_bevreage" else None}
                for k, qty in cart.items()
                for _ in range(qty)
            ]

        if item_key == "mystery_bevreage":
            revealed = random.choice(list(mystery_bevreage))
            cart.append({"key": item_key, "revealed": revealed})
            flash(f"You got {revealed}!", "mystery")
        else:
            cart.append({"key": item_key})

        session["cart"] = cart

    return redirect(url_for("index"))


@app.route("/clear", methods=["POST"])
def clear_cart():
    session["cart"] = []
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

