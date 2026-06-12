from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# ===================================
# USER MODEL
# ===================================
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(50), default="buyer")
    approved = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)

    verification_token = db.Column(db.String(255), unique=True, nullable=True)

    # RELATIONSHIPS
    products = db.relationship("Product", backref="retailer", lazy=True)
    orders = db.relationship("Order", foreign_keys="Order.user_id", backref="buyer", lazy=True)

    def set_password(self, password):
        if len(password) < 8:
            raise ValueError("Password too weak (min 8 chars)")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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

    retailer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # RELATIONSHIP
    orders = db.relationship("Order", backref="product", lazy=True)


# ===================================
# CART ITEM
# ===================================
class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    quantity = db.Column(db.Integer, default=1)


# ===================================
# ORDER MODEL (FIXED RELATIONS)
# ===================================
class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(50), default="pending")

    # IMPORTANT FIX:
    # This makes retailer dashboard work properly via JOIN
    retailer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# ===================================
# REVIEW MODEL
# ===================================
class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True)

    buyer_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    rating = db.Column(db.Integer, nullable=False)

    comment = db.Column(db.Text)

    reply = db.Column(db.Text, nullable=True)

    replied_by = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )


# ===================================
# PRIVATE CHAT
# ===================================

class Chat(db.Model):

    __tablename__="chat"

    id=db.Column(
        db.Integer,
        primary_key=True
    )

    product_id=db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=True
    )


    sender_id=db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )


    receiver_id=db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )


    message=db.Column(
        db.Text,
        nullable=False
    )



# ===================================
# PRODUCT QUESTIONS & ANSWERS
# ===================================

class ProductQuestion(db.Model):

    __tablename__ = "product_question"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )


    buyer_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )


    question = db.Column(
        db.Text,
        nullable=False
    )


    answer = db.Column(
        db.Text,
        nullable=True
    )


    answered_by = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )


    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
 

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    question = db.Column(db.Text)
    answer = db.Column(db.Text, nullable=True)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    message = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
