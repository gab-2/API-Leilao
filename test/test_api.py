import unittest
from app import app
from database import db

class AuctionAPITestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_cadastrar_item(self):
        response = self.app.post('/itens', json={'descricao': 'Item Teste', 'lance_inicial': 100.0})
        self.assertEqual(response.status_code, 201)

    def test_cadastrar_comprador(self):
        response = self.app.post('/compradores', json={'nome': 'Comprador Teste'})
        self.assertEqual(response.status_code, 201)

    def test_efetuar_lance(self):
        self.app.post('/itens', json={'descricao': 'Item Teste', 'lance_inicial': 100.0})
        self.app.post('/compradores', json={'nome': 'Comprador Teste'})
        response = self.app.post('/lances', json={'valor': 120.0, 'item_id': 1, 'comprador_id': 1})
        self.assertEqual(response.status_code, 201)

    def test_listar_itens(self):
        response = self.app.get('/itens')
        self.assertEqual(response.status_code, 200)

    def test_descricao_item(self):
        self.app.post('/itens', json={'descricao': 'Item Teste', 'lance_inicial': 100.0})
        response = self.app.get('/itens/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
