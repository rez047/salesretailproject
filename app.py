import os

from flask import Flask, render_template

from config import Config

from extensions import db, login_manager

from models import User, Product

from auth import auth, create_admin
from admin import admin_bp
from marketplace import market
from cart import cart
from chat import chat
from reviews import reviews_bp
from retailer import retailer_bp
from buyer_orders import buyer_orders
from qa import qa

from security import role_required

app = Flask(__name__)

app.config.from_object(Config)


# ==============================
# SESSION SETTINGS
# ==============================

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="LAX",
    SESSION_COOKIE_SECURE=False
)


# ==============================
# EXTENSIONS
# ==============================

db.init_app(app)

login_manager.init_app(app)

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==============================
# DATABASE INITIALIZATION
# ==============================

def init_db():

    with app.app_context():

        # Create tables
        db.create_all()


        # Create or upgrade admin
        admin_email = os.getenv("ADMIN_EMAIL")

        if admin_email:

            admin = User.query.filter_by(
                email=admin_email
            ).first()


            if admin:

                admin.role = "admin"
                admin.approved = True
                admin.is_verified = True
                admin.is_active = True

                db.session.commit()


            else:

                create_admin()



# RUN DATABASE INIT WHEN GUNICORN STARTS
with app.app_context():
    init_db()



# ==============================
# BLUEPRINTS
# ==============================

app.register_blueprint(auth)

app.register_blueprint(admin_bp)

app.register_blueprint(market)

app.register_blueprint(cart)

app.register_blueprint(chat)

app.register_blueprint(reviews_bp)

app.register_blueprint(retailer_bp)

app.register_blueprint(buyer_orders)

app.register_blueprint(qa)



# ==============================
# PAGES
# ==============================


@app.route("/")
def home():

    return render_template("login.html")



@app.route("/login")
def login_page():

    return render_template("login.html")



@app.route("/register")
def register_page():

    return render_template("register.html")



@app.route("/products-page")
def products_page():

    return render_template("products.html")



@app.route("/checkout-page")
def checkout_page():

    return render_template("checkout.html")



@app.route("/buyer")
def buyer_dashboard():

    products = Product.query.all()

    return render_template(
        "buyer_dashboard.html",
        products=products
    )



@app.route("/admin")
@role_required("admin")
def admin_dashboard():

    return render_template(
        "admin_dashboard.html"
    )



# ==============================
# LOCAL DEVELOPMENT
# ==============================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
