import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from dotenv import load_dotenv

from models import db, User

load_dotenv()

auth = Blueprint("auth", __name__)


# =========================
# LOGIN
# =========================
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # -------------------------
        # VALIDATE USER
        # -------------------------
        if user and user.check_password(password):

            # EMAIL VERIFICATION CHECK
            if not user.is_verified:
                return "Please verify your email before login", 403

            # ADMIN APPROVAL CHECK
            if not user.is_active:
                return "Account not approved by admin yet", 403

            login_user(user)

            # ROLE REDIRECTS
            if user.role == "admin":
                return redirect("/admin")

            elif user.role == "retailer":
                return redirect("/retailer")

            else:
                return redirect("/buyer")

        return "Invalid credentials", 401

    return render_template("login.html")


# =========================
# REGISTER
# =========================
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "buyer")

        # -------------------------
        # PREVENT DUPLICATES
        # -------------------------
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already exists", 400

        # -------------------------
        # CREATE USER (PENDING VERIFICATION)
        # -------------------------
        user = User(
            username=username,
            email=email,
            role=role,
            is_verified=False,
            is_active=False,
            verification_token=str(uuid.uuid4())
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # -------------------------
        # TEMP VERIFICATION OUTPUT (EMAIL SIMULATION)
        # -------------------------
        print("VERIFY USER EMAIL HERE:")
        print(f"http://127.0.0.1:5000/verify/{user.verification_token}")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# =========================
# EMAIL VERIFICATION ROUTE
# =========================
@auth.route("/verify/<token>")
def verify_email(token):

    user = User.query.filter_by(verification_token=token).first()

    if not user:
        return "Invalid or expired verification link", 400

    user.is_verified = True
    user.is_active = True
    user.verification_token = None

    db.session.commit()

    return "Email verified successfully. You can now log in."


# =========================
# CREATE ADMIN (AUTO)
# =========================
def create_admin():

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        return

    admin = User.query.filter_by(email=admin_email).first()

    if admin:
        return

    admin = User(
        username="admin",
        email=admin_email,
        role="admin",
        is_verified=True,
    )

    admin.set_password(admin_password)

    db.session.add(admin)
    db.session.commit()


# =========================
# LOGOUT
# =========================
@auth.route("/logout")
def logout():
    logout_user()
    return redirect("/")
