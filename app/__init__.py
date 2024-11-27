from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import secrets

secret_key = secrets.token_hex(16)  # Generate a random secret key

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    @app.before_request
    def create_tables():
        # The following line will remove this handler, making it
        # only run on the first request
        app.before_request_funcs[None].remove(create_tables)

        db.create_all()

    return app
