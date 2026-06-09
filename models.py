from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# ===================================
# USER MODEL
# ===================================
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        default="buyer"
    )

    approved = db.Column(
        db.Boolean,
        default=False
    )

    is_verified = db.Column(
        db.Boolean,
        default=False
    )

    verification_token = db.Column(
        db.String(255),
        unique=True,
        nullable=True
    )

    products = db.relationship(
        "Product",
        backref="retailer",
        lazy=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )


# ===================================
# PRODUCT MODEL
# ===================================
class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)

    price = db.Column(db.Float, nullable=False)

    stock = db.Column(db.Integer, default=0)

    image = db.Column(db.String(255))

    retailer_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )


# ===================================
# CART
# ===================================
class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1
    )


# ===================================
# ORDERS
# ===================================
class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    retailer_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    total_price = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )


# ===================================
# REVIEWS
# ===================================
class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True)

    buyer_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id")
    )

    rating = db.Column(db.Integer)

    comment = db.Column(db.Text)


# ===================================
# CHAT
# ===================================
class Chat(db.Model):
    __tablename__ = "chat"

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    message = db.Column(
        db.Text,
        nullable=False
    )
