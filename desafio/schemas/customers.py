dados_bancarios = {
    "type": "object",
    "properties": {
        "ag": {"type": "string", "pattern": "^[0-9]{4}$"},
        "conta": {"type": "string", "pattern": "^[0-9]{5}-[0-9Xx]{1}$"},
        "banco": {"type": "string", "minLength": 3}
    },
    "requeired": ["ag", "conta", "banco"]
}

customer_properties = {
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
}

post_schema = {
    "type": "object",
    "properties": customer_properties,
    "required": [
        "razao_social",
        "telefone",
        "endereco",
        "faturamento_declarado",
        "dados_bancarios"
    ],
    "additionalProperties": False
}

put_schema = {
    "type": "object",
    "properties": customer_properties,
    "additionalProperties": False
}