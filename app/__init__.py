from flask import Flask
from app.extensions import db, migrate, inertia

def create_app(use_inertia=True, use_migrate=True):
    app = Flask(__name__, static_url_path="", static_folder="static")
    app.config.from_object("config.Config")

    db.init_app(app)

    if use_inertia:
        inertia.init_app(app)

    if use_migrate:
        migrate.init_app(app, db, directory="app/migrations")

    from app.main import main

    app.register_blueprint(main)

    return app
