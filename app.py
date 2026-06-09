from marketplace import market
from cart import cart
from chat import chat
from reviews import reviews
from config import Config
from extensions import db, login_manager
from models import User
from auth import auth
from utils import allowed_file
from security import role_required
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(auth)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/admin")
@role_required("admin")
def admin():
    return render_template("admin_dashboard.html")

@app.route("/retailer")
def retailer():
    return "Retailer Dashboard"

@app.route("/buyer")
def buyer():
    return "Buyer Dashboard"


def create_admin():
    admin = User.query.filter_by(email="admin@shop.com").first()

    if not admin:
        admin = User(
            username="admin",
            email="admin@shop.com",
            role="admin"
        )
        admin.set_password("admin123")  # change later after login

        db.session.add(admin)
        db.session.commit()
        print("Default admin created: admin@shop.com / admin123")

app.config.from_object(Config)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="LAX",
    SESSION_COOKIE_SECURE=True  # set TRUE in production HTTPS
)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()

app.register_blueprint(market)
app.register_blueprint(cart)
app.register_blueprint(chat)
app.register_blueprint(reviews)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()

    app.run(
        host="0.0.0.0",
        port=5000
    )
