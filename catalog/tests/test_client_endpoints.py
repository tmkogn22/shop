import pytest
from rest_framework.test import APITestCase
from django.shortcuts import reverse
from pytest_conf import EVERYTHING_EQUALS_NOT_NONE

pytestmark = [pytest.mark.django_db]


class TestClientEndpoints(APITestCase):
    fixtures = ['catalog/tests/fixtures/categories_fixtures.json', 'catalog/tests/fixtures/cashback_fixtures.json',
                'catalog/tests/fixtures/discounts_fixtures.json', 'catalog/tests/fixtures/promos_fixtures.json',
                'catalog/tests/fixtures/category_products_fixtures.json', 'catalog/tests/fixtures/brands_fixtures.json']

    def test_categories_list_endpoint(self):
        url = reverse('categories')
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == [
            {'id': 1, 'name': EVERYTHING_EQUALS_NOT_NONE},
            {'id': 2, 'name': EVERYTHING_EQUALS_NOT_NONE},
            {'id': 3, 'name': EVERYTHING_EQUALS_NOT_NONE}
        ]

    def test_cashback_endpoint(self):
        url = reverse('cashback')
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == [
            {
                "id": 1,
                "percent": 10,
                "limit": 100
            }
        ]

    def test_discounts_list_endpoint(self):
        url = reverse('discounts')
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == [
            {
                "id": 1,
                "name": "discount 1",
                "start_date": "2025-03-14",
                "exp_date": "2025-03-14",
                "percent": 99
            },
            {
                "id": 2,
                "name": "discount 2",
                "start_date": "2025-03-14",
                "exp_date": "2025-03-14",
                "percent": 1
            },
            {
                "id": 3,
                "name": "discount 3",
                "start_date": "2025-03-14",
                "exp_date": "2025-03-14",
                "percent": 50
            }
        ]

    def test_promos_list_endpoint(self):
        url = reverse('promos')
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == [
            {
                "id": 1,
                "name": "promo 1",
                "percent": 100,
                "is_cumulative": False
            },
            {
                "id": 2,
                "name": "promo 2",
                "percent": 1,
                "is_cumulative": True
            },
            {
                "id": 3,
                "name": "promo 3",
                "percent": 89,
                "is_cumulative": True
            }
        ]

    def test_category_products(self):
        url = reverse('category-products', kwargs={'category_id': 3})
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == [
            {
                "id": 2,
                "article": "r2ed",
                "name": "chair",
                "price": "90.00",
                "images": []
            },
            {
                "id": 3,
                "article": "23eqwdas",
                "name": "flour",
                "price": "1.00",
                "images": []
            }
        ]

    def test_discount_products(self):
        url = reverse('discount-products', kwargs={'discount_id': 1})
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == [
            {
                "id": 2,
                "name": "chair",
                "price": "90.00",
                "article": "r2ed",
                "discount_percent": 99
            }
        ]
