from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Product, Order
from utils import allowed_file

market = Blueprint("market", __name__)

# --------------------
# ADD PRODUCT (RETAILER / ADMIN)
# --------------------
@market.route("/product/add", methods=["POST"])
@login_required
def add_product():
    if current_user.role not in ["admin", "retailer"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json

    product = Product(
        name=data["name"],
        price=data["price"],
        stock=data["stock"],
        retailer_id=current_user.id
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product added"})


# --------------------
# GET ALL PRODUCTS
# --------------------
@market.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock
        }
        for p in products
    ])


# --------------------
# PLACE ORDER
# --------------------
@market.route("/order", methods=["POST"])
@login_required
def place_order():
    data = request.json

    order = Order(
        user_id=current_user.id,
        product_id=data["product_id"],
        quantity=data["quantity"],
        total_price=0,
        status="pending"
    )

    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Order placed"})
