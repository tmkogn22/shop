import pytest
from catalog.models import Product, Cart
from rest_framework.test import APITestCase, APIClient
from django.shortcuts import reverse
from pytest_conf import EVERYTHING_EQUALS_NOT_NONE
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

pytestmark = [pytest.mark.django_db]
USER_MODEL = get_user_model()


class TestClientEndpoints(APITestCase):
    fixtures = ['catalog/tests/fixtures/categories_fixtures.json', 'catalog/tests/fixtures/cashback_fixtures.json',
                'catalog/tests/fixtures/discounts_fixtures.json', 'catalog/tests/fixtures/promos_fixtures.json',
                'catalog/tests/fixtures/category_products_fixtures.json', 'catalog/tests/fixtures/brands_fixtures.json']

    def setUp(self):
        self.client = APIClient()
        password = make_password('12345qwerty')

        self.user = USER_MODEL.objects.create(
            email='test@test.com',
            password=password,
            is_active=True
        )

        url = reverse('jwt-create')

        data = {
            'email': 'test@test.com',
            'password': '12345qwerty'
        }

        self.product = Product.objects.get(id=1)
        Cart.objects.create(user=self.user, product=self.product, amount=1)

        response = self.client.post(url, data=data, format='json')

        self.token = 'Bearer ' + response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_get_cart(self):
        url = reverse('cart')
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == {
            'products': [{'amount': 1,
                          'discounts': [{'percent': EVERYTHING_EQUALS_NOT_NONE}],
                          'name': EVERYTHING_EQUALS_NOT_NONE,
                          'price': EVERYTHING_EQUALS_NOT_NONE}]}

    def test_post_cart(self):
        start_amount = Cart.objects.get(user=self.user, product=self.product).amount
        extra_amount = 5
        url = reverse('cart')
        response = self.client.post(url, data={
            "product_id": 1,
            "amount": extra_amount
        })
        assert response.status_code == 200
        end_amount = Cart.objects.get(user=self.user, product=self.product).amount
        assert start_amount == (end_amount - extra_amount)

    def test_delete_cart(self):
        url = reverse('cart')
        response = self.client.delete(url, data={'product_id': 1})
        assert response.status_code == 200
        assert list(Cart.objects.filter(product=self.product, user=self.user)) == []

