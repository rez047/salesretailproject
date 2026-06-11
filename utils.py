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
# EMAIL FUNCTION (FIXED)
# =========================
def send_verification_email(email, token):

    verify_url = f"https://theemiratesretailstore777.onrender.com/verify/{token}"

    try:
        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": email,
            "subject": "Verify your email",
            "html": f"""
            <h2>Verify your account</h2>
            <p>Click below to verify your account:</p>
            <a href="{verify_url}">Verify Email</a>
            """
        })

        print("EMAIL SENT SUCCESS:", response)
        return response

    except Exception as e:
        # IMPORTANT: prevents registration from breaking
        print("EMAIL FAILED (NON-FATAL):", str(e))
        print("VERIFY LINK (MANUAL):", verify_url)

        # still allow user to register
        return {
            "status": "failed",
            "error": str(e),
            "verify_url": verify_url
        }
