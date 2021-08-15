import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

db = SQLAlchemy()
redis_db = redis.Redis(
    host=config('REDIS_HOST'),
    port=config('REDIS_PORT'),
    db=config('REDIS_DB')
)
