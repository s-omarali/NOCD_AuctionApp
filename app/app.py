from flask import Flask
from routes.listing_routes import listing_bp
from routes.bid_routes import bid_bp
from routes.auth import auth_bp  
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")


    jwt = JWTManager(app)

    # Register Blueprints
    app.register_blueprint(listing_bp, url_prefix='/listings')
    app.register_blueprint(bid_bp, url_prefix='/bids')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/')
    def home():
        return "Bidding App API is running!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)