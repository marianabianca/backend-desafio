from flask import Flask
from desafio.database.models import db
import os

# create and configure the app
app = Flask(__name__, instance_relative_config=True)

# initialize db
app.config['MONGODB_SETTINGS'] = [
    {
        "db": os.environ.get('DATABASE_NAME'),
        "host": os.environ.get("DATABASE_HOST"),
        "port": int(os.environ.get("DATABASE_PORT")),
        "username": os.environ.get("DATABASE_USERNAME"),
        "password": os.environ.get("DATABASE_PASSWORD")
    }
]

db.init_app(app)

# register routes
from desafio.routes.customers import customers_bp
app.register_blueprint(customers_bp, url_prefix="/clientes")

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
