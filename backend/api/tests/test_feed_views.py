from rest_framework import status

from utils.testcase import TestCase


class UserTests(TestCase):
    url = "/api/feed/"

    def test_list_view(self):

        user = self.create_user()
        token = self.create_token(user)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_feed_with_valid_data(self):

        user = self.create_user()
        token = self.create_token(user)

        data = {"url": "http://www.nu.nl/rss/Algemeen", "title": "NU.NL"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_feed_with_invalid_url(self):

        user = self.create_user()
        token = self.create_token(user)

        data = {"url": "http://www.google.com", "title": "Google"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
