from flask_mongoengine import MongoEngine

db = MongoEngine()

class DadosBancarios(db.EmbeddedDocument):
    ag = db.StringField(required=True)
    conta = db.StringField(required=True)
    banco = db.StringField(required=True)


class Customer(db.Document):
    razao_social = db.StringField(required=True)
    telefone = db.StringField(required=True)
    endereco = db.StringField(required=True)
    faturamento_declarado = db.IntField(required=True)
    dados_bancarios = db.EmbeddedDocumentListField(
        document_type=DadosBancarios,
        required=True
    )
    data_cadastro = db.StringField(required=True)
    ultima_atualizacao = db.StringField()

