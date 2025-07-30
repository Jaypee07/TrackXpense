import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
from .routes import main

# Load environment variables from .env
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Flask-Login user loader
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Factory pattern to create the app
def create_app():
    app = Flask(__name__)

    # Load configs from environment or use default values
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_dev_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///trackxpense.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(main)

    return app
