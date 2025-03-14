import pytest
from rest_framework.test import APITestCase
from django.shortcuts import reverse
from pytest_conf import EVERYTHING_EQUALS_NOT_NONE

pytestmark = [pytest.mark.django_db]


class TestClientEndpoints(APITestCase):
    fixtures = ['catalog/tests/fixtures/categories_fixtures.json']

    def test_categories_list_endpoint(self):
        url = reverse('categories')
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data == [
            {'id': 1, 'name': EVERYTHING_EQUALS_NOT_NONE},
            {'id': 2, 'name': EVERYTHING_EQUALS_NOT_NONE},
            {'id': 3, 'name': EVERYTHING_EQUALS_NOT_NONE}
        ]
