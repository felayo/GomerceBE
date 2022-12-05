import json
import unittest

from models import Product
from models.abc import db
from repositories import ProductRepository
from server import server

new_product = {
    'title' : 'Phone', 
    'quantity' : 10,
    'short_desc' : "A mobile phone"
}

class TestProduct(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get(self):
        """ The GET on `/product` should return an customer """
        ProductRepository.create(new_product)
        response = self.client.get("/products")

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode("utf-8"))
        self.assertTrue(response_json.data['all_products'])

    def test_create(self):
        """ The POST on `/product` should create an customer """
        response = self.client.post(
            "/products/create_product",
            content_type="application/json",
            json={new_product}
        )

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode("utf-8"))
        self.assertTrue(response_json.data['data'])

    """ def test_update(self):
        The PUT on `/customer` should update an customer's age
        UserRepository.create(first_name="John", last_name="Doe", age=25)
        response = self.client.put(
            "/application/customer/Doe/John",
            content_type="application/json",
            data=json.dumps({"age": 30}),
        )

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode("utf-8"))
        self.assertEqual(
            response_json,
            {"customer": {"age": 30, "first_name": "John", "last_name": "Doe"}},
        )
        user = UserRepository.get(first_name="John", last_name="Doe")
        self.assertEqual(user.age, 30) """