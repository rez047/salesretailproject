from models import db, User
import os


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
        approved=True,
        is_verified=True,
        is_active=True
    )

    admin.set_password(admin_password)

    db.session.add(admin)
    db.session.commit()
