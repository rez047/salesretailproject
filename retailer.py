from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models import db, Order, Product

retailer_bp = Blueprint("retailer", __name__)


# =====================================
# RETAILER DASHBOARD
# =====================================

@retailer_bp.route("/retailer/dashboard")
@login_required
def dashboard():

    orders = Order.query.filter_by(
        retailer_id=current_user.id
    ).all()

    products = Product.query.filter_by(
        retailer_id=current_user.id
    ).all()

    return render_template(
        "retailer_dashboard.html",
        orders=orders,
        products=products
    )


# =====================================
# UPDATE ORDER STATUS
# =====================================

@retailer_bp.route(
    "/retailer/order/<int:order_id>/status",
    methods=["POST"]
)
@login_required
def update_status(order_id):

    order = Order.query.get(order_id)

    if not order:
        return "Order not found", 404

    status = request.form.get("status")

    order.status = status

    db.session.commit()

    return redirect(
        url_for("retailer.dashboard")
    )


# =====================================
# RETAILER PRODUCTS
# =====================================

@retailer_bp.route("/retailer/products")
@login_required
def products():

    products = Product.query.filter_by(
        retailer_id=current_user.id
    ).all()

    return render_template(
        "retailer_products.html",
        products=products
    )
