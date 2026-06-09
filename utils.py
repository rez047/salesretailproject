import os
from resend import Resend

# =========================
# FILE UPLOAD HELPERS (optional)
# =========================
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# =========================
# EMAIL (RESEND SERVICE)
# =========================

resend.api_key = os.getenv("RESEND_API_KEY")


def send_verification_email(to_email, token):
    """
    Sends verification email using Resend API.
    """

    verify_url = f"https://emiratessales888.onrender.com/verify/{token}"

    response = resend_client.emails.send({
        "from": "Emirates Shop <onboarding@resend.dev>",
        "to": [to_email],
        "subject": "Verify your account",
        "html": f"""
            <h2>Verify Your Account</h2>
            <p>Click the link below to verify your email:</p>
            <a href="{verify_url}">{verify_url}</a>
        """
    })

    return response
