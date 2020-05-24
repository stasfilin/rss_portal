import random

from rest_framework import status

from utils.testcase import TestCase


class CommentTests(TestCase):
    """
    Comment API Test Case
    """

    url = "/api/comment/"
    headers = {"Content-Type": "application/json", "Accept-Encoding": None}

    def test_post_comment_with_valid_data(self):
        """
        Test adding new comment with valid data
        """
        user = self.create_user()
        token = self.create_token(user)
        feed = self.create_feed(user)
        feed_item = self.create_feed_item(feed, user)

        data = {"feed_item": feed_item.pk, "content": "Test Comment"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get("content", ""), data.get("content"))

    def test_post_comment_with_invalid_feed_item(self):
        """
        Test adding new comment with invalid feed item
        """
        user = self.create_user()
        token = self.create_token(user)

        data = {"feed_item": random.randint(1, 10), "content": "Test Comment"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_comment_with_valid_data(self):
        """
        Test delete comment with valid data
        """
        user = self.create_user()
        token = self.create_token(user)
        feed = self.create_feed(user)
        feed_item = self.create_feed_item(feed, user)

        data = {"feed_item": feed_item.pk, "content": "Test Comment"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get("content", ""), data.get("content"))

        response = self.client.delete(
            self.url + str(response.json().get("id")) + "/", headers=self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
