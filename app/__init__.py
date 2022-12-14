from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.price import Price
    from app.models.stock import Stock
    

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from app.routes import stocks_bp
   
    
    
    # app.register_blueprint(prices_bp)
    app.register_blueprint(stocks_bp)
    


    CORS(app)
    return app
