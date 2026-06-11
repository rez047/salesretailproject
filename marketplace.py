from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from models import Product, Order
from extensions import db


market = Blueprint("market", __name__)


# ==============================
# ADD PRODUCT (ADMIN / RETAILER)
# ==============================
@market.route("/product/add", methods=["POST"])
@login_required
def add_product():

    if current_user.role not in ["admin", "retailer"]:
        return jsonify({"error": "Unauthorized"}), 403


    # Accept JSON API requests
    if request.is_json:
        data = request.get_json()

        name = data.get("name")
        price = data.get("price")
        stock = data.get("stock")

    # Accept normal HTML forms too
    else:
        name = request.form.get("name")
        price = request.form.get("price")
        stock = request.form.get("stock")


    if not name or not price or not stock:
        return jsonify({
            "error": "Missing product details"
        }), 400


    product = Product(
        name=name,
        price=float(price),
        stock=int(stock),
        retailer_id=current_user.id
    )


    db.session.add(product)
    db.session.commit()


    return jsonify({
        "message": "Product added successfully"
    })



# ==============================
# VIEW PRODUCTS
# ==============================
@market.route("/products", methods=["GET"])
def get_products():

    products = Product.query.all()


    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock,
            "retailer": p.retailer.username
        }

        for p in products
    ])




# ==============================
# PLACE ORDER
# ==============================
@market.route("/order", methods=["POST"])
@login_required
def place_order():


    if request.is_json:
        data = request.get_json()
    else:
        data = request.form


    product = Product.query.get(
        data.get("product_id")
    )


    if not product:
        return jsonify({
            "error": "Product not found"
        }),404



    quantity = int(
        data.get("quantity",1)
    )


    order = Order(
        user_id=current_user.id,
        retailer_id=product.retailer_id,
        product_id=product.id,
        quantity=quantity,
        total_price=product.price * quantity,
        status="Pending"
    )


    db.session.add(order)
    db.session.commit()


    return jsonify({
        "message":"Order placed"
    })
