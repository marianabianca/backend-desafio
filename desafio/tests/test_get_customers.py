import unittest
import json

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



    def tearDown(self):
        # Delete Database collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)