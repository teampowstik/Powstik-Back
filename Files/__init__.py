from flask import Flask
from Files.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS

ma=Marshmallow()

db=SQLAlchemy()

def createApp(configClass = Config):
    app = Flask(__name__)
    app.config.from_object(configClass)
    cors = CORS(app, resources={r"/foo": {"origins": "*"}})
    cors = CORS(app, resources={r"/api": {"origins": "http://localhost:3000"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    db.init_app(app)

    JWTManager(app)

    from Files.user.routes import user
    app.register_blueprint(user)

    from Files.product.routes import product
    app.register_blueprint(product)
    
    from Files.consultations.routes import consultation_blueprint
    app.register_blueprint(consultation_blueprint)
    
    from Files.category.routes import category_blueprint
    app.register_blueprint(category_blueprint)

    from Files.seller.routes import seller
    app.register_blueprint(seller)

    from Files.orders.routes import orders_blueprint
    app.register_blueprint(orders_blueprint)

    from Files.cart.routes import cart_blueprint
    app.register_blueprint(cart_blueprint)

    from Files.wishlist.routes import wishlist_blueprint
    app.register_blueprint(wishlist_blueprint)

    from Files.authenticaion.routes import authentication
    app.register_blueprint(authentication)
    
    from Files.address.routes import address
    app.register_blueprint(address)

    with app.app_context():
        db.create_all()
    
    return app