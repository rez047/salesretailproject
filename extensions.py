from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from utils import allowed_file

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"