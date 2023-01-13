from flask import Flask
import os
from pymongo import MongoClient

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # initialize db
    global db
    mongo = MongoClient(
            os.environ.get("DATABASE_HOST"),
            int(os.environ.get("DATABASE_PORT")),
            username = os.environ.get("DATABASE_USERNAME"),
            password = os.environ.get("DATABASE_PASSWORD")
        )
    db = mongo.desafio_backend

    # register routes
    from desafio.routes.customers import customers_bp
    app.register_blueprint(customers_bp, url_prefix="/clientes")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

