from flask import Flask, jsonify
from models import db
from routes.order_routes import order_bp
from routes.product_routes import product_bp
from routes.restaurant_routes import restaurant_bp

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)



app.register_blueprint(restaurant_bp, url_prefix='/api/v1/restaurants')
app.register_blueprint(product_bp, url_prefix='/api/v1/products')
app.register_blueprint(order_bp, url_prefix='/api/v1/orders')
@app.route('/')
def home():
    return {
        "message": "Restaurant API radi",
        "version": "v1"
    }
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
