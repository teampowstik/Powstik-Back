from flask import Flask
from Files.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

ma=Marshmallow()

db=SQLAlchemy()

def createApp(configClass = Config):
    app = Flask(__name__)
    app.config.from_object(configClass)

    
    db.init_app(app)

    from Files.user.routes import user
    app.register_blueprint(user)

    # from Files.product.routes import product
    # app.register_blueprint(product)

    with app.app_context():
        db.create_all()
    
    return app