from flask_restx import Api

from app.ping.api.v1 import ping_namespace

api = Api(version="1.0", title="Auth API")

api.add_namespace(ping_namespace, path="/ping")
