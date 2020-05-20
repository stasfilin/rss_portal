from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from faker import Faker
from rest_framework.test import APITestCase
from rest_framework_jwt.utils import jwt_create_payload, jwt_encode_payload


class TestCase(APITestCase):
    faker = Faker()

    def create_user(self):
        user_password = get_random_string()
        user_data = {
            "username": self.faker.first_name(),
            "password": user_password,
            "email": self.faker.email(),
        }
        user = User.objects.create_user(**user_data)

        return user

    def create_token(self, user):
        payload = jwt_create_payload(user)
        token = jwt_encode_payload(payload)
        return token
