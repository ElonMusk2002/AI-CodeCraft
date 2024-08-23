# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def truncatewords(value, num_words):
    words = value.split()
    if len(words) > num_words:
        return " ".join(words[:num_words]) + "..."
    return value


def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.jinja_env.filters["truncatewords"] = truncatewords

    from app.routes import bp as routes_bp

    app.register_blueprint(routes_bp)

    return app
