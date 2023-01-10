from flask import Flask, request
from pymongo import MongoClient
from flask_expects_json import expects_json
from datetime import datetime
from bson import json_util, ObjectId
import os

app = Flask(__name__)

client = MongoClient(
    os.environ.get("DATABASE_HOST"),
    int(os.environ.get("DATABASE_PORT")),
    username = os.environ.get("DATABASE_USERNAME"),
    password = os.environ.get("DATABASE_PASSWORD")
    )

db = client.desafio_backend
customers = db.customers

dados_bancarios = {
    "type": "object",
    "properties": {
        "ag": {"type": "string", "pattern": "^[0-9]{4}$"},
        "conta": {"type": "string", "pattern": "^[0-9]{5}-[0-9Xx]{1}$"},
        "banco": {"type": "string", "minLength": 3}
    },
    "requeired": ["ag", "conta", "banco"]
}

post_schema = {
    "type": "object",
    "properties": {
        "razao_social": {"type": "string"},
        "telefone": {
            "type": "string",
            "pattern": "^([0-9]{2,3})?([0-9]{2})([0-9]{4,5})([0-9]{4})$"
        },
        "endereco": {
            "type": "string",
            "minLength": 3  
        },
        "faturamento_declarado": {
            "type": "number",
            "minimum": 0
        },
        "dados_bancarios": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": dados_bancarios
        }
    },
    "required": [
        "razao_social",
        "telefone",
        "endereco",
        "faturamento_declarado",
        "dados_bancarios"
    ]
}

def get_customer_by_id(id):
    id = ObjectId(id)
    customer = customers.find_one({"_id": id})
    return customer


@app.route("/clientes", methods=['POST'])
@expects_json(post_schema)
def create_new_customer():
    customer = request.json
    now = datetime.now()
    customer["data_cadastro"] = now.isoformat()
    print(type(customer))
    print(customer)

    inserted_id = customers.insert_one(customer).inserted_id
    return json_util.dumps(get_customer_by_id(inserted_id))


@app.route("/clientes", methods=['GET'])
def get_all_customers():
    result = customers.find()
    return json_util.dumps(result)


@app.route("/clientes/<id>", methods=['GET'])
def get_customer(id):
    if ObjectId.is_valid(id):
        response = get_customer_by_id(id)
        if response != None:
            return json_util.dumps(response)
        return "Customer not found", 404
    return "Invalid ID format", 422


@app.route("/clientes/<id>", methods=['PUT'])
def update_customer(id):
    return id
    

@app.route("/clientes/<id>", methods=['DELETE'])
def delete_customer(id):
    return id
