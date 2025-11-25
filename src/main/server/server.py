from dotenv import load_dotenv

load_dotenv(".env")

from flask import Flask
from flask_cors import CORS

from src.main.routes.report_routes import report_routes_bp

from src.model.settings.mongo_db_connection import mongo_db_connection

mongo_db_connection.connect()

app = Flask(__name__)
CORS(app)

app.register_blueprint(report_routes_bp)