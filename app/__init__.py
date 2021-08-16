from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

from app.settings import config
from app.api import api


db = SQLAlchemy()
admin = Admin(template_mode="bootstrap3")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app_settings = (
        config('APP_SETTINGS')
        if config('APP_SETTINGS', default=None)
        else f"app.settings.{config('FLASK_ENV').title()}Config"
    )
    app.config.from_object(app_settings)

    db.init_app(app)
    if config('FLASK_ENV') == "development":
        admin.init_app(app)

    api.init_app(app)

    return app
