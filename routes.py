from flask import request, jsonify
from models import Item, Comprador, Lance
from database import db_session
from datetime import datetime
from flask_swagger import swagger 
from flask import jsonify  

def setup_routes(app):

    @app.route('/spec')
    def spec():
        return jsonify(swagger(app))

    @app.route('/itens', methods=['POST'])
    def cadastrar_item():
        data = request.get_json()
        item = Item(descricao=data['descricao'], lance_inicial=data['lance_inicial'])
        db_session.add(item)
        db_session.commit()
        return jsonify({'id': item.id}), 201

    @app.route('/compradores', methods=['POST'])
    def cadastrar_comprador():
        data = request.get_json()
        comprador = Comprador(nome=data['nome'])
        db_session.add(comprador)
        db_session.commit()
        return jsonify({'id': comprador.id}), 201

    @app.route('/lances', methods=['POST'])
    def efetuar_lance():
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
        itens = Item.query.all()
        response = [{'id': item.id, 'descricao': item.descricao, 'maior_lance': (item.lances[-1].valor if item.lances else item.lance_inicial), 'tempo_restante': (item.tempo_leilao - datetime.utcnow()).total_seconds()} for item in itens]
        return jsonify(response)

    @app.route('/itens/<int:id>', methods=['GET'])
    def descricao_item(id):
        item = Item.query.get(id)
        if item:
            response = {'id': item.id, 'descricao': item.descricao, 'maior_lance': (item.lances[-1].valor if item.lances else item.lance_inicial), 'tempo_restante': (item.tempo_leilao - datetime.utcnow()).total_seconds()}
            return jsonify(response)
        return jsonify({'erro': 'Item não encontrado'}), 404
