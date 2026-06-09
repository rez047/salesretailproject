import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "temporary-development-key-change-me"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///retailshop.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False