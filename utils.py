import os
from dotenv import load_dotenv
from mailjet_rest import Client

load_dotenv()


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
# MAILJET CONFIG
# =========================
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")

mailjet = Client(
    auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY),
    version="v3.1"
)


# =========================
# EMAIL FUNCTION (MAILJET)
# =========================
def send_verification_email(email, token):

    verify_url = f"https://theemiratesretailstore777.onrender.com/verify/{token}"

    data = {
        "Messages": [
            {
                "From": {
                    "Email": "no-reply@emiratesretailshop.com",
                    "Name": "Emirates Retailshop"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": email
                    }
                ],
                "Subject": "Verify your Emirates Retailshop account",
                "HTMLPart": f"""
                    <h2>Welcome to Emirates Retailshop</h2>
                    <p>Please verify your account by clicking below:</p>
                    <a href="{verify_url}">Verify Email</a>
                """
            }
        ]
    }

    try:
        result = mailjet.send.create(data=data)

        print("MAILJET RESPONSE:", result.status_code, result.json())
        return result.json()

    except Exception as e:
        print("MAILJET ERROR:", str(e))
        print("VERIFY LINK (MANUAL):", verify_url)

        return {
            "status": "failed",
            "error": str(e),
            "verify_url": verify_url
        }
