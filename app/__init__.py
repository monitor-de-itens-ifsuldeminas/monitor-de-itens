from flask import Flask
from dotenv import load_dotenv
from app.database import init_db
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    init_db(app)

    # As rotas serão registradas aqui posteriormente

    return app