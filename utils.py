import os
import resend

# =========================
# FILE UPLOAD HELPERS
# =========================
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# =========================
# RESEND CONFIG
# =========================
resend.api_key = os.getenv("RESEND_API_KEY")


# =========================
# EMAIL FUNCTION
# =========================
def send_verification_email(email, token):

    verify_url = f"https://emirates-6l9y.onrender.com/verify/{token}"

    response = resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": email,
        "subject": "Verify your email",
        "html": f"""
        <h2>Verify your account</h2>
        <p>Click below to verify:</p>
        <a href="{verify_url}">Verify Email</a>
        """
    })

    return response
