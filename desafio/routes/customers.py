from flask import request, Blueprint
from flask_expects_json import expects_json
from datetime import datetime
from bson import json_util, ObjectId
from desafio.schemas.customers import post_schema, put_schema, dados_bancarios
from desafio.errors.exceptions import InvalidIDException, ContentNotFoundException, APIException
from desafio import db

customers_bp = Blueprint("clientes", __name__)

customers = db.customers

def handle_exception(err):
    response = {
        "error": err.message,
        "status": err.status
    }
    return json_util.dumps(response), err.status


def get_customer_by_id(id):
    if not ObjectId.is_valid(id):
        raise InvalidIDException()
    id = ObjectId(id)
    customer = customers.find_one({"_id": id})
    if customer == None:
        raise ContentNotFoundException()
    return customer


def set_last_update(object):
    now = datetime.now()
    object['ultima_atualizacao'] = now.isoformat()


@customers_bp.route("/", methods=['POST'])
@expects_json(post_schema)
def create_new_customer():
    customer = request.json
    now = datetime.now()
    customer["data_cadastro"] = now.isoformat()

    inserted_id = customers.insert_one(customer).inserted_id
    return json_util.dumps(get_customer_by_id(inserted_id)), 201


@customers_bp.route("/", methods=['GET'])
def get_all_customers():
    result = customers.find()
    return json_util.dumps(result)


@customers_bp.route("/<id>", methods=['GET'])
def get_customer(id):
    try:
        customer = get_customer_by_id(id)
    except APIException as e:
        return handle_exception(e)
        
    return json_util.dumps(customer)


@customers_bp.route("/<id>", methods=['PUT'])
@expects_json(put_schema)
def update_customer(id):
    try:
        get_customer_by_id(id)
    except APIException as e:
        return handle_exception(e)
    
    update = request.json
    set_last_update(update)
    filter = {"_id": ObjectId(id)}
    customers.update_one(filter, {"$set": update}).raw_result

    return json_util.dumps(get_customer_by_id(id))


@customers_bp.route("/dados-bancarios/<id>", methods=['PUT'])
@expects_json(dados_bancarios)
def add_bank_accounts(id):
    try:
        customer = get_customer_by_id(id)
    except APIException as e:
        return handle_exception(e)
    
    bank_accounts = request.json
    
    for bank_account in bank_accounts:
        if bank_account not in customer['dados_bancarios']:
            customer['dados_bancarios'].append(bank_account)

    set_last_update(customer)
    filter = {"_id": ObjectId(id)}
    customers.update_one(filter, {"$set": customer}).raw_result

    return json_util.dumps(customer)
    

@customers_bp.route("/<id>", methods=['DELETE'])
def delete_customer(id):
    try:
        get_customer_by_id(id)
    except APIException as e:
        return handle_exception(e)
        
    customers.delete_one({"_id": ObjectId(id)})
    return "", 204

