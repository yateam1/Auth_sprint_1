from flask_restx import reqparse

headers_parser = reqparse.RequestParser()

headers_parser.add_argument('Authorization', location='headers')
headers_parser.add_argument('User-Agent', location='headers')
headers_parser.add_argument('Fingerprint', location='headers')
