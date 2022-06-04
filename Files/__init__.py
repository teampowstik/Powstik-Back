from flask import Flask
from Files.config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def createApp(configClass = Config):
    app = Flask(__name__)
    app.config.from_object(configClass)

    db.init_app(app)

    from Files.user.routes import user
    app.register_blueprint(user)

    with app.app_context():
        db.create_all()
    
    return app