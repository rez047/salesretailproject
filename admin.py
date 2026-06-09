from flask import Blueprint, render_template, redirect, request
from flask_login import login_required
from models import User, Product, Order
from extensions import db

admin_bp = Blueprint("admin", __name__)


def role_required(role):
    def wrapper(func):
        from functools import wraps

        @wraps(func)
        def decorated(*args, **kwargs):
            from flask_login import current_user

            if not current_user.is_authenticated or current_user.role != role:
                return "Unauthorized", 403

            return func(*args, **kwargs)

        return decorated
    return wrapper


@admin_bp.route("/admin")
@login_required
@role_required("admin")
def dashboard():
    users = User.query.all()
    products = Product.query.all()
    orders = Order.query.all()
    return render_template(
        "admin_dashboard.html",
        users=users,
        products=products,
        orders=orders
    )


# ---------------- USERS ----------------

@admin_bp.route("/delete_user/<int:id>")
@login_required
@role_required("admin")
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect("/admin")


# ---------------- RETAILERS ----------------

@admin_bp.route("/approve_retailer/<int:id>")
@login_required
@role_required("admin")
def approve_retailer(id):
    user = User.query.get(id)
    if user and user.role == "retailer":
        user.approved = True
        db.session.commit()
    return redirect("/admin")


# ---------------- PRODUCTS ----------------

@admin_bp.route("/add_product", methods=["POST"])
@login_required
@role_required("admin")
def add_product():
    name = request.form["name"]
    price = request.form["price"]
    stock = request.form["stock"]

    product = Product(name=name, price=price, stock=stock)
    db.session.add(product)
    db.session.commit()

    return redirect("/admin")


@admin_bp.route("/delete_product/<int:id>")
@login_required
@role_required("admin")
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect("/admin")
