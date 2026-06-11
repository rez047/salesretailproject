from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user

from models import db, Product, CartItem, Order

cart = Blueprint("cart", __name__)


# =========================
# ADD TO CART (INCREASE QTY)
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


# =========================
# VIEW CART (FULL FIXED)
# =========================
@cart.route("/cart")
@login_required
def view_cart():

    items = CartItem.query.filter_by(
        user_id=current_user.id
    ).all()

    cart_items = []
    total = 0

    for item in items:

        product = Product.query.get(item.product_id)

        if not product:
            continue

        subtotal = product.price * item.quantity
        total += subtotal

        cart_items.append({
            "id": item.id,
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "subtotal": subtotal,
            "image": product.image
        })

    return render_template(
        "cart.html",
        items=cart_items,
        total=total
    )


# =========================
# REMOVE ITEM
# =========================
@cart.route("/cart/remove/<int:item_id>")
@login_required
def remove_item(item_id):

    item = CartItem.query.get(item_id)

    if item and item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()

    return redirect(url_for("cart.view_cart"))


# =========================
# CHECKOUT (NO JS)
# =========================
@cart.route("/checkout", methods=["POST"])
@login_required
def checkout():

    cart_items = CartItem.query.filter_by(
        user_id=current_user.id
    ).all()

    if not cart_items:
        return "Cart is empty", 400

    for item in cart_items:

        product = Product.query.get(item.product_id)

        if not product:
            continue

        order = Order(
            user_id=current_user.id,
            product_id=product.id,
            quantity=item.quantity,
            total_price=product.price * item.quantity,
            status="pending",
            retailer_id=product.retailer_id
        )

        db.session.add(order)
        db.session.delete(item)

    db.session.commit()

    return redirect(url_for("cart.view_cart"))
