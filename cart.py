from flask import Blueprint, session, request, jsonify
from utils import allowed_file

cart = Blueprint("cart", __name__)

# --------------------
# ADD TO CART (SESSION BASED)
# --------------------
@cart.route("/cart/add", methods=["POST"])
def add_to_cart():
    data = request.json

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append({
        "product_id": data["product_id"],
        "quantity": data["quantity"]
    })

    session.modified = True

    return jsonify({"message": "Added to cart"})


# --------------------
# VIEW CART
# --------------------
@cart.route("/cart", methods=["GET"])
def view_cart():
    return jsonify(session.get("cart", []))


# --------------------
# CLEAR CART
# --------------------
@cart.route("/cart/clear", methods=["POST"])
def clear_cart():
    session["cart"] = []
    return jsonify({"message": "Cart cleared"})