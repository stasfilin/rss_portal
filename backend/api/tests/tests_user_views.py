from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework import status

from utils.testcase import TestCase


class UserTests(TestCase):
    def test_valid_signup(self):
        url = "/api/signup/"

        user_password = get_random_string()
        data = {
            "username": self.faker.first_name(),
            "password": user_password,
            "email": self.faker.email(),
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signin(self):
        url = "/api/signin/"

        user_password = get_random_string()
        user_data = {
            "username": self.faker.first_name(),
            "password": user_password,
            "email": self.faker.email(),
        }
        user = User.objects.create_user(**user_data)

        data = {
            "username": user.username,
            "password": user_password,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
