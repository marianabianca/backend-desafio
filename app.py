from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)

client = MongoClient(
    os.environ.get("DATABASE_HOST"),
    int(os.environ.get("DATABASE_PORT")),
    username = os.environ.get("DATABASE_USERNAME"),
    password = os.environ.get("DATABASE_PASSWORD")
    )

db = client.flask_db
clients = db.clients

@app.route("/clientes", methods=['POST'])
def create_new_client():
    return 'new client'

@app.route("/clientes", methods=['GET'])
def get_all_clients():
    return 'clients'

@app.route("/clientes/<id>", methods=['GET'])
def get_client(id):
    return id

@app.route("/clientes/<id>", methods=['PUT'])
def update_client(id):
    return id

@app.route("/clientes/<id>", methods=['DELETE'])
def delete_client(id):
    return id