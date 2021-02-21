import unittest

from flask import url_for, current_app

from app import create_app
from app.models import DIDNumber
from app.serializers import DIDNumberSchema


class EndpointsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/testing.db'
        })
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.drop_all()

    def test_endpoint_of_numbers_with_empty_list(self):
        response = self.client.get(url_for('numbers.list_numbers')).json
        self.assertEqual(response, []) 

    def test_endpoint_of_numbers_with_one_element_in_the_list(self):
        data = {
            'value': '1234234234',
            'monthy_price': '11.44',
            'setup_price': '455.55',
            'currency': 'R$' 
        }
        serializer = DIDNumberSchema()
        number = serializer.load(data)
        self.app.db.session.add(number)
        self.app.db.session.commit()
        response = self.client.get(url_for('numbers.list_numbers')).json
        response_expected = [
            {
                'currency': 'R$', 
                'id': 1, 
                'monthy_price': 11.44, 
                'setup_price': 455.55, 
                'value': '1234234234'}
        ]
        self.assertEqual(response, response_expected) 