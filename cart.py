from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user
from models import db, Product, CartItem, Order

cart = Blueprint("cart", __name__)


# =========================
# ADD TO CART (DB-BASED)
# =========================
@cart.route("/cart/add/<int:product_id>")
@login_required
def add_to_cart(product_id):

    item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if item:
        item.quantity += 1
    else:
        item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(item)

    db.session.commit()

    return redirect(url_for("cart.view_cart"))

@cart.route("/checkout", methods=["POST"])
@login_required
def checkout():

    cart_items = session.get("cart", [])

    for item in cart_items:

        product = Product.query.get(item["product_id"])

        order = Order(
            user_id=current_user.id,
            product_id=product.id,
            quantity=item["quantity"],
            total_price=product.price * item["quantity"],
            status="pending"
        )

        db.session.add(order)

    db.session.commit()

    session["cart"] = []

    return "Order placed successfully"
    
# =========================
# VIEW CART
# =========================
@cart.route("/cart")
@login_required
def view_cart():

    items = CartItem.query.filter_by(user_id=current_user.id).all()

    cart_data = []

    total = 0

    for item in items:
        product = Product.query.get(item.product_id)

        subtotal = product.price * item.quantity
        total += subtotal

        cart_data.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "items": cart_data,
        "total": total
    }


# =========================
# REMOVE ITEM FROM CART
# =========================
@cart.route("/cart/remove/<int:product_id>")
@login_required
def remove_from_cart(product_id):

    item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if item:
        db.session.delete(item)
        db.session.commit()

    return redirect(url_for("cart.view_cart"))

