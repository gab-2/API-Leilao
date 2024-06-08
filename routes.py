from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from models import Item, Comprador, Lance
from database import db_session
from datetime import datetime

app = Flask(__name__)
api = Api(app, version='1.0', title='Auction API', description='API de um Leilão')

item_model = api.model('Item', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an item'),
    'descricao': fields.String(required=True, description='Item description'),
    'lance_inicial': fields.Float(required=True, description='Initial bid value'),
})

comprador_model = api.model('Comprador', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a buyer'),
    'nome': fields.String(required=True, description='Buyer name'),
})

lance_model = api.model('Lance', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a bid'),
    'valor': fields.Float(required=True, description='Bid value'),
    'item_id': fields.Integer(required=True, description='The ID of the item being bid on'),
    'comprador_id': fields.Integer(required=True, description='The ID of the buyer making the bid'),
})

@api.route('/itens')
class ItemList(Resource):
    @api.doc('list_items')
    @api.marshal_list_with(item_model)
    def get(self):
        """List all items"""
        itens = Item.query.all()
        response = [{'id': item.id, 'descricao': item.descricao, 'maior_lance': (item.lances[-1].valor if item.lances else item.lance_inicial), 'tempo_restante': (item.tempo_leilao - datetime.utcnow()).total_seconds()} for item in itens]
        return response

    @api.doc('create_item')
    @api.expect(item_model)
    @api.marshal_with(item_model, code=201)
    def post(self):
        """Create a new item"""
        data = request.get_json()
        item = Item(descricao=data['descricao'], lance_inicial=data['lance_inicial'])
        db_session.add(item)
        db_session.commit()
        return item, 201

@api.route('/itens/<int:id>')
@api.response(404, 'Item not found')
@api.param('id', 'The item identifier')
class Item(Resource):
    @api.doc('get_item')
    @api.marshal_with(item_model)
    def get(self, id):
        """Fetch an item given its identifier"""
        item = Item.query.get(id)
        if item:
            response = {'id': item.id, 'descricao': item.descricao, 'maior_lance': (item.lances[-1].valor if item.lances else item.lance_inicial), 'tempo_restante': (item.tempo_leilao - datetime.utcnow()).total_seconds()}
            return response
        api.abort(404)

@api.route('/compradores')
class CompradorList(Resource):
    @api.doc('create_comprador')
    @api.expect(comprador_model)
    @api.marshal_with(comprador_model, code=201)
    def post(self):
        """Create a new buyer"""
        data = request.get_json()
        comprador = Comprador(nome=data['nome'])
        db_session.add(comprador)
        db_session.commit()
        return comprador, 201

@api.route('/lances')
class LanceList(Resource):
    @api.doc('create_lance')
    @api.expect(lance_model)
    @api.marshal_with(lance_model, code=201)
    def post(self):
        """Create a new bid"""
        data = request.get_json()
        lance = Lance(valor=data['valor'], item_id=data['item_id'], comprador_id=data['comprador_id'])
        item = Item.query.get(data['item_id'])
        if item and lance.valor > (item.lances[-1].valor if item.lances else item.lance_inicial):
            db_session.add(lance)
            db_session.commit()
            return lance, 201
        api.abort(400, 'Invalid bid')

if __name__ == '__main__':
    app.run(debug=True)
