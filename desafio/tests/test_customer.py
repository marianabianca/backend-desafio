
import unittest
import json
import bson

from desafio.database.models import db
from dotenv import load_dotenv

load_dotenv(".env.test", override=True)

from desafio.app import app

class CustomerTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.get_db()
        self.post_payload = {
            "razao_social": "nome empresa",
            "telefone": "558399999999",
            "endereco": "rua exemplo",
            "faturamento_declarado": 10000,
            "dados_bancarios": [
                {
                    "ag": "0000",
                    "conta": "00000-9",
                    "banco": "nome banco"
                }
            ]
        }


    def test_successful_create_customer(self):
        # Given
        payload = json.dumps(self.post_payload)

        # When
        response = self.app.post('/clientes/', headers={"Content-Type": "application/json"}, data=payload)
        response_body = response.data.decode()

        # Then
        self.assertTrue('_id' in response_body)
        self.assertEqual(201, response.status_code)

    
    def test_unsuccessful_create_customer_missing_property(self):
        # Given payload missing razao_social
        payload = json.dumps({
            "telefone": "558399999999",
            "endereco": "rua exemplo",
            "faturamento_declarado": 10000,
            "dados_bancarios": [
                {
                    "ag": "0000",
                    "conta": "00000-9",
                    "banco": "nome banco"
                }
            ]
        })

        # When
        response = self.app.post('/clientes/', headers={"Content-Type": "application/json"}, data=payload)
        response_body = response.data.decode()

        # Then
        self.assertTrue('razao_social' in response_body)
        self.assertEqual(400, response.status_code)


    def test_unsuccessful_create_customer_idditional_property(self):
        # Given payload with an additional property
        payload = json.dumps({
            "additional": "property",
            "razao_social": "nome empresa",
            "telefone": "558399999999",
            "endereco": "rua exemplo",
            "faturamento_declarado": 10000,
            "dados_bancarios": [
                {
                    "ag": "0000",
                    "conta": "00000-9",
                    "banco": "nome banco"
                }
            ]
        })

        # When
        response = self.app.post('/clientes/', headers={"Content-Type": "application/json"}, data=payload)
        response_body = response.data.decode()

        # # Then
        self.assertTrue('additionalProperties' in response_body)
        self.assertEqual(400, response.status_code)


    def test_successful_get_all_customers_empty(self):
        # When
        response = self.app.get('/clientes/', headers={"Content-Type": "application/json"})
        response_body = json.loads(response.data.decode())

        # Then
        self.assertEqual(0, len(response_body))
        self.assertEqual(200, response.status_code)


    def test_successful_get_all_customers(self):
        # adding customer to db
        payload = json.dumps(self.post_payload)
        self.app.post('/clientes/', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = self.app.get('/clientes/', headers={"Content-Type": "application/json"})
        response_body = json.loads(response.data.decode())

        # Then
        self.assertEqual(1, len(response_body))
        self.assertEqual(200, response.status_code)


    def test_successful_get_customer_by_id(self):
        # adding customer to db
        payload = json.dumps(self.post_payload)
        post_response = self.app.post('/clientes/', headers={"Content-Type": "application/json"}, data=payload)
        post_response_body = json.loads(post_response.data.decode())
        customer_id = post_response_body['_id']['$oid']

        # Given
        path = '/clientes/' + customer_id

        # When
        response = self.app.get(path, headers={"Content-Type": "application/json"})
        response_body = json.loads(response.data.decode())

        # Then
        self.assertEqual(customer_id, response_body['_id']['$oid'])
        self.assertEqual(200, response.status_code)


    def test_unsuccessful_get_customer_by_id_invalid_id(self):
        # Given
        customer_id = 123

        path = '/clientes/' + str(customer_id)

        # When
        response = self.app.get(path, headers={"Content-Type": "application/json"})
        response_body = json.loads(response.data.decode())

        # Then
        self.assertEqual("Invalid ID format", response_body["error"])
        self.assertEqual(422, response_body["status"])
        self.assertEqual(422, response.status_code)


    def test_unsuccessful_get_customer_by_id_not_found(self):
        customer_id = bson.ObjectId()

        path = '/clientes/' + str(customer_id)

        # When
        response = self.app.get(path, headers={"Content-Type": "application/json"})
        response_body = json.loads(response.data.decode())

        # Then
        self.assertEqual("Content not found", response_body["error"])
        self.assertEqual(404, response_body["status"])
        self.assertEqual(404, response.status_code)


    def tearDown(self):
        # Delete Database collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)