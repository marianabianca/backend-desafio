# backend-desafio
Desafio de programação de backend

# Pre requisitos
- Tenha Python 3 instalado na máquina
- Tenha o MongoDB instalado na máquina
- Configure o MongoDB

# Como executar

## Antes da primeira execução
- Crie um arquivo `.env` com as mesmas variáveis que estão no arquivo `.env.example`.
 Essas variáveis são as informações necessárias para que a aplicação de conecte ao
 banco de dados MongoDB
- Crie também um arquivo `.env.test` com as mesmas variáveis que estão no `.env.test.example`.
 Da mesma forma que o `.env`, essas variáveis irão ser usadas para que a aplicação se conecte
 ao banco de dados MongoDB, mas nesse caso, será um banco de dados de teste, então lembre-se 
 de que o nome do banco de dados do `.env.test` deve ser diferente do `.env`

## Primeira execução
- No diretório raiz do repositório, crie um ambiente virtual utilizando o comando no terminal:
`python3 -m venv venv`
- Entre no ambiente virtual, dentro do diretório raiz, utilizando o comando: `venv\Scripts\activate`
- Então, instale as bibliotecas necessárias com o seguinte comando:
`pip install -r requirements.txt`
- Para iniciar o servidor, rode, ainda dentro do ambiente virtual, o comando: `flask --app desafio/run --debug run`

## Execuções seguintes

- Entre no ambiente virtual, dentro do diretório raiz, utilizando o comando: `venv\Scripts\activate`
- Para iniciar o servidor, rode, ainda dentro do ambiente virtual, o comando: `flask --app desafio/run --debug run`

## Como finalizar a execução

- Para finalizar a execução do Flask, você pode utilizar `CTRL+c`
- Para sair do ambiente virtual, utilize o comando: `deactivate`

## Como rodar os testes

- Na pasta raiz do repositório, rode o comando `python -m unittest discover desafio/tests`

# Documentação Swagger

[https://app.swaggerhub.com/apis/marianabianca/desafio_backend/1.0.0](https://app.swaggerhub.com/apis/marianabianca/desafio_backend/1.0.0)
