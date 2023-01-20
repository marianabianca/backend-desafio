from flask import request, Blueprint
from flask_expects_json import expects_json
from datetime import datetime
from bson import json_util, ObjectId
from desafio.schemas.customers import post_schema, put_schema, dados_bancarios
from desafio.errors.exceptions import InvalidIDException, ContentNotFoundException, APIException
import desafio.database.models as models
import json

customers_bp = Blueprint("clientes", __name__)

def handle_exception(err):
    response = {
        "error": err.message,
        "status": err.status
    }
    return json_util.dumps(response), err.status


def get_customer_by_id(id):
    if not ObjectId.is_valid(id):
        raise InvalidIDException()
    try:
        customer = models.Customer.objects().get(id=id)
    except:
        raise ContentNotFoundException()
    return customer.to_json()


def set_last_update(object):
    now = datetime.now()
    object['ultima_atualizacao'] = now.isoformat()


@customers_bp.route("/", methods=['POST'])
@expects_json(post_schema)
def create_new_customer():
    customer = request.get_json()
    now = datetime.now()
    customer["data_cadastro"] = now.isoformat()

    new_customer = models.Customer(**customer).save()
    return new_customer.to_json(), 201


@customers_bp.route("/", methods=['GET'])
def get_all_customers():
    result = models.Customer.objects()
    return result.to_json()


@customers_bp.route("/<id>", methods=['GET'])
def get_customer(id):
    try:
        customer = get_customer_by_id(id)
    except APIException as e:
        return handle_exception(e)
        
    return customer


@customers_bp.route("/<id>", methods=['PUT'])
@expects_json(put_schema)
def update_customer(id):
    try:
        get_customer_by_id(id)
    except APIException as e:
        return handle_exception(e)
    
    update = request.get_json()
    set_last_update(update)
    models.Customer.objects(id=id).update(**update)

    return '', 200


@customers_bp.route("/dados-bancarios/<id>", methods=['PUT'])
@expects_json(dados_bancarios)
def add_bank_accounts(id):
    try:
        customer = get_customer_by_id(id)
    except APIException as e:
        return handle_exception(e)
    
    bank_accounts = request.get_json()
    customer = json.loads(customer)

    for bank_account in bank_accounts:
        if bank_account not in customer['dados_bancarios']:
            customer['dados_bancarios'].append(bank_account)

    set_last_update(customer)

    models.Customer.objects(id=id).update(
        dados_bancarios = customer['dados_bancarios'],
        ultima_atualizacao = customer['ultima_atualizacao']
    )

    return '', 200


@customers_bp.route("/<id>", methods=['DELETE'])
def delete_customer(id):
    try:
        get_customer_by_id(id)
    except APIException as e:
        return handle_exception(e)
        
    models.Customer.objects(id=id).delete()
    return "", 204

