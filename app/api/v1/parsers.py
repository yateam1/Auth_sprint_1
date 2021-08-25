from flask_restx import Namespace

general_namespace = Namespace('general')

headers_parser = general_namespace.parser()
headers_parser.add_argument('Authorization', location='headers')
headers_parser.add_argument('User-Agent', location='headers')
headers_parser.add_argument('Fingerprint', location='headers')
