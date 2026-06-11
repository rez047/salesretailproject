from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Order

buyer_orders = Blueprint("buyer_orders", __name__)


@buyer_orders.route("/buyer/orders")
@login_required
def order_history():

    orders = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(Order.id.desc()).all()

    return render_template(
        "buyer_orders.html",
        orders=orders
    )
