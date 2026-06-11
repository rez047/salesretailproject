from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models import db, Order, Product, User

retailer_bp = Blueprint("retailer", __name__)


# =====================================
# RETAILER DASHBOARD (FIXED WORKING QUERY)
# =====================================
@retailer_bp.route("/retailer/dashboard")
@login_required
def dashboard():

    orders = (
        db.session.query(Order)
        .join(Product)
        .all()
    )

    products = Product.query.all()

    return render_template(
        "retailer_dashboard.html",
        orders=orders,
        products=products
    )


# =====================================
# UPDATE ORDER STATUS (SAFE)
# =====================================
@retailer_bp.route("/retailer/order/<int:order_id>/status", methods=["POST"])
@login_required
def update_status(order_id):

    order = Order.query.get(order_id)

    if not order:
        return "Order not found", 404

    # 🔥 SECURITY CHECK
    if order.product.retailer_id != current_user.id:
        return "Unauthorized", 403

    order.status = request.form.get("status")

    db.session.commit()

    return redirect(url_for("retailer.dashboard"))
