import os


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
# OPTIONAL APP HELPERS
# =========================

def get_upload_folder():

    return os.path.join(
        "static",
        "uploads"
    )
