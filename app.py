from flask import Flask, request
from pymongo import MongoClient
from flask_expects_json import expects_json
from datetime import datetime
from bson import json_util, ObjectId
from schemas.customer import post_schema, put_schema
from errors.exceptions import InvalidIDException, ContentNotFoundException, APIException
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
    if not ObjectId.is_valid(id):
        raise InvalidIDException()
    id = ObjectId(id)
    customer = customers.find_one({"_id": id})
    if customer == None:
        raise ContentNotFoundException()
    return customer


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
    try:
        customer = get_customer_by_id(id)
    except APIException as e:
        return json_util.dumps(e.message), e.status
        
    return json_util.dumps(customer)


@app.route("/clientes/<id>", methods=['PUT'])
@expects_json(put_schema)
def update_customer(id):
    try:
        get_customer_by_id(id)
    except APIException as e:
        return json_util.dumps(e.message), e.status
    
    update = request.json
    now = datetime.now()
    update['ultima_atualizacao'] = now.isoformat()
    filter = {"_id": ObjectId(id)}

    customers.update_one(filter, {"$set": update}).raw_result
    return json_util.dumps(get_customer_by_id(id))
    

@app.route("/clientes/<id>", methods=['DELETE'])
def delete_customer(id):
    try:
        get_customer_by_id(id)
    except APIException as e:
        return json_util.dumps(e.message), e.status
        
    customers.delete_one({"_id": ObjectId(id)})
    return "", 204

