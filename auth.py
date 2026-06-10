import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from dotenv import load_dotenv

from models import db, User
from utils import send_verification_email

load_dotenv()

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

        if not user:
            return "Invalid credentials", 401


        if not user.check_password(password):
            return "Invalid credentials", 401


        # ==========================
        # ADMIN BYPASS
        # ==========================
        if user.role == "admin":

            user.is_active = True
            db.session.commit()

            login_user(user)

            return redirect("/admin")


        # ==========================
        # NORMAL USERS
        # ==========================
        if not user.is_verified:
            return "Verify your email first."


        if not user.approved:
            return "Waiting for admin approval."


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
        role = request.form.get("role")

        existing = User.query.filter_by(email=email).first()

        if existing:
            return "Email already exists"

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

        send_verification_email(user.email, user.verification_token)

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ===================================
# VERIFY EMAIL
# ===================================

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
    


# ===================================
# CREATE ADMIN
# ===================================
def create_admin():

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        return


    admin = User.query.filter_by(
        email=admin_email
    ).first()


    if admin:

        admin.role="admin"
        admin.approved=True
        admin.is_verified=True
        admin.is_active=True

        db.session.commit()

        print("Existing admin updated")

        return



    admin = User(
        username="admin",
        email=admin_email,
        role="admin",
        approved=True,
        is_verified=True,
        is_active=True
    )


    admin.set_password(admin_password)


    db.session.add(admin)
    db.session.commit()


    print("Admin account created")


# ===================================
# LOGOUT
# ===================================
@auth.route("/logout")
def logout():

    logout_user()

    return redirect("/")
