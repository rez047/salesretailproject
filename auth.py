import os
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from models import db, User
from dotenv import load_dotenv
load_dotenv()

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            login_user(user)

            if user.role == "admin":
                return redirect("/admin")
            elif user.role == "retailer":
                return redirect("/retailer")
            else:
                return redirect("/buyer")

        return "Invalid credentials", 401

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        # 🔥 PREVENT DUPLICATE EMAILS
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already exists", 400

        user = User(username=username, email=email, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")

def create_admin():
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    print("ADMIN EMAIL FROM ENV:", admin_email)
    print("ADMIN PASSWORD FROM ENV:", admin_password)

    admin = User.query.filter_by(email=admin_email).first()

    if admin:
        print("Admin already exists")
        return

    admin = User(
        username="admin",
        email=admin_email,
        role="admin"
    )

    admin.set_password(admin_password)

    db.session.add(admin)
    db.session.commit()

    print("Admin created successfully")


@auth.route("/logout")
def logout():
    logout_user()
    return redirect("/")