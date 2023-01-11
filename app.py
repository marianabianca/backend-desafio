from flask import Flask, request
from pymongo import MongoClient
from flask_expects_json import expects_json
from datetime import datetime
from bson import json_util, ObjectId
from schemas import post_schema, put_schema
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

def get_customer_by_id(id):
    id = ObjectId(id)
    customer = customers.find_one({"_id": id})
    return customer


def validate_id(id):
    if not ObjectId.is_valid(id):
        return "Invalid ID format", 422
    response = get_customer_by_id(id)
    if response == None:
        return "Customer not found", 404


@app.route("/clientes", methods=['POST'])
@expects_json(post_schema)
def create_new_customer():
    customer = request.json
    now = datetime.now()
    customer["data_cadastro"] = now.isoformat()

    inserted_id = customers.insert_one(customer).inserted_id
    return json_util.dumps(get_customer_by_id(inserted_id))


@app.route("/clientes", methods=['GET'])
def get_all_customers():
    result = customers.find()
    return json_util.dumps(result)


@app.route("/clientes/<id>", methods=['GET'])
def get_customer(id):
    invalid_id = validate_id(id)
    if invalid_id:
        return invalid_id

    response = get_customer_by_id(id)
    return json_util.dumps(response)


@app.route("/clientes/<id>", methods=['PUT'])
@expects_json(put_schema)
def update_customer(id):
    invalid_id = validate_id(id)
    if invalid_id:
        return invalid_id
    
    update = request.json
    now = datetime.now()
    update['ultima_atualizacao'] = now.isoformat()
    filter = {"_id": ObjectId(id)}

    customers.update_one(filter, {"$set": update})
    return json_util.dumps(get_customer_by_id(id))
    

@app.route("/clientes/<id>", methods=['DELETE'])
def delete_customer(id):
    invalid_id = validate_id(id)
    if invalid_id:
        return invalid_id
    customers.delete_one({"_id": ObjectId(id)})
    return "", 204

