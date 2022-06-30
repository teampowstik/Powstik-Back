from flask import Flask
from Files.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

ma=Marshmallow()

db=SQLAlchemy()

def createApp(configClass = Config):
    app = Flask(__name__)
    app.config.from_object(configClass)

    
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

    with app.app_context():
        db.create_all()
    
    return app