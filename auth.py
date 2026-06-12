import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from models import db, User

auth = Blueprint("auth", __name__)


# ===================================
# LOGIN
# ===================================
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return "Invalid credentials", 401

        # ADMIN
        if user.role == "admin":
            user.is_active = True
            db.session.commit()
            login_user(user)
            return redirect("/admin")

        # VERIFY CHECK
        if not user.is_verified:
            return "Please verify your account first", 403

        # APPROVAL CHECK
        if not user.approved:
            return "Waiting for admin approval", 403

        user.is_active = True
        db.session.commit()

        login_user(user)

        if user.role == "retailer":
            return redirect("/retailer/dashboard")

        return redirect("/buyer")

    return render_template("login.html")


# ===================================
# REGISTER
# ===================================
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role") or "buyer"

        existing = User.query.filter_by(email=email).first()

        if existing:
            return "Email already exists", 400

        token = str(uuid.uuid4())

        user = User(
            username=username,
            email=email,
            role=role,
            approved=False,
            is_verified=False,
            verification_token=token
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        verify_url = url_for("auth.verify_email", token=token, _external=True)

        return f"""
        <html>
        <body style="font-family:Arial;text-align:center;padding:40px;">
            <h2>Registration Successful</h2>
            <p>Verify your account:</p>
            <a href="{verify_url}">Verify Account</a>
        </body>
        </html>
        """

    return render_template("register.html")


# ===================================
# VERIFY EMAIL
# ===================================
@auth.route("/verify/<token>")
def verify_email(token):

    user = User.query.filter_by(verification_token=token).first()

    if not user:
        return "Invalid or expired link", 400

    user.is_verified = True
    user.is_active = True
    user.verification_token = None

    db.session.commit()

    return """
    <h2>Verified successfully</h2>
    <a href="/login">Login</a>
    """


# ===================================
# LOGOUT
# ===================================
@auth.route("/logout")
def logout():

    logout_user()
    return redirect("/")
