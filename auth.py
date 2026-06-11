import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from dotenv import load_dotenv

from models import db, User


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
            return "Please verify your account first."


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
        role = request.form.get("role") or "buyer"


        existing = User.query.filter_by(
            email=email
        ).first()


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



        # ==========================
        # DIRECT VERIFICATION LINK
        # NO EMAIL REQUIRED
        # ==========================

        verify_url = url_for(
            "auth.verify_email",
            token=token,
            _external=True
        )


        return f"""
        <!DOCTYPE html>

        <html>

        <head>
            <title>Verify Account</title>

            <style>

            body {{
                font-family: Arial;
                background:#f4f6f9;
                padding:40px;
                text-align:center;
            }}

            .box {{
                background:white;
                padding:30px;
                border-radius:10px;
                max-width:500px;
                margin:auto;
                box-shadow:0 2px 10px #ccc;
            }}

            a {{
                background:#0b3d91;
                color:white;
                padding:12px 20px;
                text-decoration:none;
                border-radius:5px;
            }}

            </style>

        </head>


        <body>


        <div class="box">

        <h2>Registration Successful</h2>

        <p>Your account has been created.</p>

        <p>Click below to verify your account:</p>


        <br>


        <a href="{verify_url}">
        Verify Account
        </a>


        <br><br>


        <p>
        After verification you can login.
        </p>


        <a href="/login">
        Go To Login
        </a>


        </div>


        </body>

        </html>
        """


    return render_template("register.html")



# ===================================
# VERIFY ACCOUNT
# ===================================

@auth.route("/verify/<token>")
def verify_email(token):

    user = User.query.filter_by(
        verification_token=token
    ).first()


    if not user:
        return "Invalid or expired verification link", 400



    user.is_verified = True

    user.is_active = True

    user.verification_token = None


    db.session.commit()


    return """
    <h2>
    Account verified successfully.
    </h2>

    <p>
    You can now login.
    </p>

    <a href="/login">
    Login
    </a>
    """




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

        admin.role = "admin"
        admin.approved = True
        admin.is_verified = True
        admin.is_active = True

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
