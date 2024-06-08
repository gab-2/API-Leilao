from flask import Flask, request, jsonify
from models import Item, Comprador, Lance
from database import db_session
from datetime import datetime
from flask_swagger import swagger  
from flask_swagger_ui import get_swaggerui_blueprint  

app = Flask(__name__)

def setup_routes(app):

    @app.route('/spec')
    def spec():
        swag = swagger(app, from_file_keyword='swagger_from_file')
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "API de Leilão"
        return jsonify(swag)

    SWAGGER_URL = '/swagger'
    API_URL = '/spec'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "API de Leilão"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/itens', methods=['POST'])
    def cadastrar_item():
        """
        Cadastra um novo item para leilão
        ---
        tags:
          - itens
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - descricao
                - lance_inicial
              properties:
                descricao:
                  type: string
                lance_inicial:
                  type: number
        responses:
          201:
            description: Item cadastrado com sucesso
          400:
            description: Erro na requisição
        """
        data = request.get_json()
        item = Item(descricao=data['descricao'], lance_inicial=data['lance_inicial'])
        db_session.add(item)
        db_session.commit()
        return jsonify({'id': item.id}), 201

    @app.route('/compradores', methods=['POST'])
    def cadastrar_comprador():
        """
        Cadastra um novo comprador
        ---
        tags:
          - compradores
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - nome
              properties:
                nome:
                  type: string
        responses:
          201:
            description: Comprador cadastrado com sucesso
          400:
            description: Erro na requisição
        """
        data = request.get_json()
        comprador = Comprador(nome=data['nome'])
        db_session.add(comprador)
        db_session.commit()
        return jsonify({'id': comprador.id}), 201

    @app.route('/lances', methods=['POST'])
    def efetuar_lance():
        """
        Efetua um novo lance em um item de leilão
        ---
        tags:
          - lances
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - valor
                - item_id
                - comprador_id
              properties:
                valor:
                  type: number
                item_id:
                  type: integer
                comprador_id:
                  type: integer
        responses:
          201:
            description: Lance efetuado com sucesso
          400:
            description: Lance inválido
        """
        data = request.get_json()
        lance = Lance(valor=data['valor'], item_id=data['item_id'], comprador_id=data['comprador_id'])
        item = Item.query.get(data['item_id'])
        if item and lance.valor > (item.lances[-1].valor if item.lances else item.lance_inicial):
            db_session.add(lance)
            db_session.commit()
            return jsonify({'id': lance.id}), 201
        return jsonify({'erro': 'Lance inválido'}), 400

    @app.route('/itens', methods=['GET'])
    def listar_itens():
        """
        Lista todos os itens de leilão
        ---
        tags:
          - itens
        responses:
          200:
            description: Lista de itens
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  descricao:
                    type: string
                  maior_lance:
                    type: number
                  tempo_restante:
                    type: number
        """
        itens = Item.query.all()
        response = [{'id': item.id, 'descricao': item.descricao, 'maior_lance': (item.lances[-1].valor if item.lances else item.lance_inicial), 'tempo_restante': (item.tempo_leilao - datetime.utcnow()).total_seconds()} for item in itens]
        return jsonify(response)

    @app.route('/itens/<int:id>', methods=['GET'])
    def descricao_item(id):
        """
        Retorna a descrição de um item específico
        ---
        tags:
          - itens
        parameters:
          - in: path
            name: id
            required: true
            type: integer
        responses:
          200:
            description: Descrição do item
            schema:
              type: object
              properties:
                id:
                  type: integer
                descricao:
                  type: string
                maior_lance:
                  type: number
                tempo_restante:
                  type: number
          404:
            description: Item não encontrado
        """
        item = Item.query.get(id)
        if item:
            response = {'id': item.id, 'descricao': item.descricao, 'maior_lance': (item.lances[-1].valor if item.lances else item.lance_inicial), 'tempo_restante': (item.tempo_leilao - datetime.utcnow()).total_seconds()}
            return jsonify(response)
        return jsonify({'erro': 'Item não encontrado'}), 404

setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
