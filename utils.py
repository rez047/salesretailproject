
import os
import resend

resend.api_key = os.getenv("re_8gx5tnEB_61hzHWncpE4U7fWs8LRGFFJp")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def send_verification_email(to_email, token):
    verification_link = f"https://your-app.onrender.com/verify/{token}"

    resend.Emails.send({
        "from": "Shop System <onboarding@resend.dev>",
        "to": to_email,
        "subject": "Verify your account",
        "html": f"""
            <h2>Verify Your Account</h2>
            <p>Click the link below to activate your account:</p>
            <a href="{verification_link}">Verify Email</a>
        """
    })




