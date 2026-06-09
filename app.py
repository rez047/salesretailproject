from flask import Flask, render_template
from config import Config

from extensions import db, login_manager
from models import User

from auth import auth, create_admin
from admin import admin_bp
from marketplace import market
from cart import cart
from chat import chat
from reviews import reviews

from security import role_required

from retailer import retailer_bp

# =========================
# APP INIT
# =========================
app = Flask(__name__)
app.config.from_object(Config)

# Security (sessions)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="LAX",
    SESSION_COOKIE_SECURE=False  # set True ONLY on HTTPS (Render later)
)

# =========================
# EXTENSIONS INIT
# =========================
db.init_app(app)
login_manager.init_app(app)


# =========================
# BLUEPRINTS
# =========================
app.register_blueprint(auth)
app.register_blueprint(admin_bp)
app.register_blueprint(cart)
app.register_blueprint(market)
app.register_blueprint(chat)
app.register_blueprint(reviews)
app.register_blueprint(retailer_bp)

# =========================
# USER LOADER
# =========================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =========================
# PAGES (FRONTEND ROUTES)
# =========================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/products-page")
def products_page():
    return render_template("products.html")


@app.route("/cart")
def cart_page():
    return render_template("cart.html")


@app.route("/checkout")
def checkout_page():
    return render_template("checkout.html")


# =========================
# ROLE ROUTES
# =========================
@app.route("/admin")
@role_required("admin")
def admin():
    return render_template("admin_dashboard.html")


@retailer_bp.route("/retailer/dashboard")
@login_required
def dashboard():

    orders = Order.query.filter_by(retailer_id=current_user.id).all()

    return render_template("retailer_dashboard.html", orders=orders)


@app.route("/buyer")
@login_required
def buyer():
    products = Product.query.all()
    return render_template("buyer_dashboard.html", products=products)


@retailer_bp.route("/retailer/order/<int:order_id>/status", methods=["POST"])
@login_required
def update_status(order_id):

    order = Order.query.get(order_id)

    if not order:
        return "Order not found", 404

    new_status = request.form.get("status")

    order.status = new_status

    db.session.commit()

    return redirect("/retailer/dashboard")

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

    return redirect("/cart")

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
            "id": item.id,
            "name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return render_template("cart.html", items=cart_data, total=total)


@cart.route("/cart/remove/<int:item_id>")
@login_required
def remove_item(item_id):

    item = CartItem.query.get(item_id)

    if item:
        db.session.delete(item)
        db.session.commit()

    return redirect("/cart")


@cart.route("/checkout", methods=["POST"])
@login_required
def checkout():

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        return "Cart is empty", 400

    for item in cart_items:

        product = Product.query.get(item.product_id)

        order = Order(
            user_id=current_user.id,
            product_id=product.id,
            quantity=item.quantity,
            total_price=product.price * item.quantity,
            status="pending",
            retailer_id=product.retailer_id if hasattr(product, "retailer_id") else None
        )

        db.session.add(order)

        db.session.delete(item)

    db.session.commit()

    return redirect("/buyer")
    
# =========================
# DATABASE INIT (CLEAN)
# =========================
def init_db():
    with app.app_context():
        db.create_all()
        create_admin()


init_db()


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
