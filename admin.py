import os
import uuid

from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import User, Product, Order
from extensions import db
from utils import allowed_file


admin_bp = Blueprint("admin", __name__)


UPLOAD_FOLDER = "static/uploads/products"


# =========================
# ROLE PROTECTION
# =========================
def role_required(role):
    from functools import wraps

    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                return "Unauthorized", 403
            return func(*args, **kwargs)
        return decorated
    return wrapper


# =========================
# DASHBOARD
# =========================
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


# =========================
# USERS
# =========================
@admin_bp.route("/delete_user/<int:id>")
@login_required
@role_required("admin")
def delete_user(id):

    user = User.query.get(id)

    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect("/admin")


@admin_bp.route("/approve_user/<int:id>")
@login_required
@role_required("admin")
def approve_user(id):

    user = User.query.get(id)

    if not user:
        return redirect("/admin")

    # Do NOT allow approving admins (safety)
    if user.role == "admin":
        return redirect("/admin")

    # Approve BOTH buyers and retailers
    user.approved = True
    user.is_verified = True
    user.is_active = True

    db.session.commit()

    return redirect("/admin")


# =========================
# PRODUCTS (WITH IMAGE UPLOAD)
# =========================
@admin_bp.route("/add_product", methods=["POST"])
@login_required
@role_required("admin")
def add_product():

    name = request.form.get("name")
    price = request.form.get("price")
    stock = request.form.get("stock")

    image_file = request.files.get("image")
    image_filename = None


    # =========================
    # OPTIONAL IMAGE UPLOAD
    # =========================
    if image_file and image_file.filename != "":

        if allowed_file(image_file.filename):

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            filename = secure_filename(image_file.filename)

            unique_filename = str(uuid.uuid4()) + "_" + filename

            image_path = os.path.join(UPLOAD_FOLDER, unique_filename)

            image_file.save(image_path)

            image_filename = unique_filename


    product = Product(
        name=name,
        price=float(price),
        stock=int(stock),
        image=image_filename,
        retailer_id=current_user.id
    )

    db.session.add(product)
    db.session.commit()

    return redirect("/admin")


# =========================
# DELETE PRODUCT
# =========================
@admin_bp.route("/delete_product/<int:id>")
@login_required
@role_required("admin")
def delete_product(id):

    product = Product.query.get(id)

    if product:
        db.session.delete(product)
        db.session.commit()

    return redirect("/admin")
