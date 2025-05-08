from flask import Flask
from routes.listing_routes import listing_bp
from routes.bid_routes import bid_bp

app = Flask(__name__)
app.register_blueprint(listing_bp)
app.register_blueprint(bid_bp)
@app.route('/')
def home():
    return "Bidding App API is running!"


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

