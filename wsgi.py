from app import app

# This exposes the Flask app as a WSGI callable for production servers
application = app

if __name__ == "__main__":
    application.run()