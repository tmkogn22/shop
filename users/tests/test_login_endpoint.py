import pytest
from rest_framework.test import APIClient, APITestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


USER_MODEL = get_user_model()


pytestmark = [pytest.mark.django_db]


class TestLoginEndpoint(APITestCase):

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

        response = self.client.post(url, data=data, format='json')

        self.token = 'Bearer ' + response.data['access']

    def test_login_endpoint(self):
        url = reverse('test-login')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data['message'] == 'jkndfsadkjqnewmdas'

