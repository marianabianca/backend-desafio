from flask import Flask

app = Flask(__name__)

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