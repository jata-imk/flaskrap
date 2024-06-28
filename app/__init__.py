from flask import Flask
from flask_inertia import Inertia
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
inertia = Inertia()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db, directory='app/migrations')
    inertia.init_app(app)

    from app.main import main
    app.register_blueprint(main)

    return app