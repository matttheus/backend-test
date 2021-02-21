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

    def test__LISTING_endpoint_of_numbers_with_empty_list(self):
        response = self.client.get(url_for('numbers.list_numbers')).json
        self.assertEqual(response['results'], []) 

    def test_LISTING_endpoint_of_numbers_with_one_element_in_the_list(self):
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
        response_expected = [{
            'currency': 'R$', 
            'id': 1, 
            'monthy_price': 11.44, 
            'setup_price': 455.55, 
            'value': '1234234234'
        }]
        self.assertEqual(response['results'], response_expected) 

    def test_pagination_query_params_of_LISTING_endpoint_of_numbers_with_10_elements_in_the_database(self):
        self.create_x_total_of_numbers()
        response = self.client.get(
            f"{url_for('numbers.list_numbers')}?page=2&per_page=5").json
        self.assertEqual(len(response['results']), 5)

    def test_total_of_numbers_listing_should_be_max_of_20_even_if_the_database_has_more(self):
        self.create_x_total_of_numbers(30)
        response = self.client.get(
            f"{url_for('numbers.list_numbers')}").json
        self.assertEqual(len(response['results']), 20)

    def test_CREATE_number_using_endpoint_with_valid_data(self):
        data = {
            'currency': 'R$', 
            'monthy_price': 11.44, 
            'setup_price': 455.55, 
            'value': '1234234234'
        }
        response = self.client.post(
            url_for('numbers.create_number'), 
            json=data
        ).json
        data.update({"id": 1})
        expected_response = data
        self.assertEqual(response, expected_response)

    def test_status_code_201_when_create_a_number_successfully(self):
        data = {
            'currency': 'R$', 
            'monthy_price': 11.44, 
            'setup_price': 455.55, 
            'value': '1234234234'
        }
        response = self.client.post(
            url_for('numbers.create_number'), 
            json=data
        )
        self.assertEqual(response.status_code, 201)

    def test_error_message_when_setup_price_is_not_provided(self):
        data = {
            'currency': 'R$', 
            'monthy_price': 11.44, 
            'value': '1234234234'
        }
        response = self.client.post(
            url_for('numbers.create_number'), 
            json=data
        ).json
        error_message = {'setup_price': ['Missing data for required field.']}
        self.assertEqual(response, error_message)

    def test_status_code_400_when_setup_price_is_not_provided(self):
        data = {
            'currency': 'R$', 
            'monthy_price': 11.44, 
            'value': '1234234234'
        }
        response = self.client.post(
            url_for('numbers.create_number'), 
            json=data
        )
        self.assertEqual(response.status_code, 400)
    
    def create_x_total_of_numbers(self, total: int = 10):
        for _ in range(total):
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