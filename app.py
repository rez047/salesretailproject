from flask import Flask, render_template

from config import Config
from extensions import db, login_manager
from models import User, Product


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)


    # ==============================
    # SESSION SECURITY
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
    # DATABASE
    # ==============================

    with app.app_context():

        db.create_all()

        from seed import create_admin
        create_admin()



    # ==============================
    # BLUEPRINTS
    # ==============================


    from auth import auth
    from admin import admin_bp
    from marketplace import market
    from cart import cart
    from chat import chat
    from reviews import reviews_bp
    from retailer import retailer_bp
    from buyer_orders import buyer_orders
    from qa import qa



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



    @app.route("/buyer")
    def buyer_dashboard():

        products = Product.query.all()

        return render_template(
            "buyer_dashboard.html",
            products=products
        )



    @app.route("/products-page")
    def products_page():

        return render_template("products.html")



    @app.route("/checkout-page")
    def checkout_page():

        return render_template("checkout.html")



    return app



app = create_app()



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
