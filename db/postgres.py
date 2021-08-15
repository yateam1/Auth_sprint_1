from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

SQLALCHEMY_DATABASE_URI = f"""postgresql://
    {config('POSTGRES_USERNAME')}:
    {config('POSTGRES_PASSWORD')}@
    {config('POSTGRES_HOST')}/
    {config('POSTGRES_DB')
}"""

db = SQLAlchemy()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)

