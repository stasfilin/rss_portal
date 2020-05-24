import json
import os
from unittest import mock

import feedparser
from rest_framework import status

from utils.testcase import TestCase


class FeedTests(TestCase):
    """
    Feed API Test Case
    """

    url = "/api/feed/"

    def test_list_view(self):
        """
        Test API request for getting all feeds
        """
        user = self.create_user()
        token = self.create_token(user)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_feed_with_valid_data(self):
        """
        Test for creating new feed via API with valid data
        """
        user = self.create_user()
        token = self.create_token(user)

        data = {"url": "http://www.nu.nl/rss/Algemeen", "title": "NU.NL"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_feed_with_invalid_url(self):
        """
        Test for creating new feed via API with invalid data
        """
        user = self.create_user()
        token = self.create_token(user)

        data = {"url": "http://www.google.com", "title": "Google"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fetch_feed(self):
        """
        Test for fetch feed manually by user
        """
        user = self.create_user()
        token = self.create_token(user)

        data = {"url": "http://www.nu.nl/rss/Algemeen", "title": "NU.NL"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        feed_id = response.json().get("id")
        response = self.client.get(self.url + str(feed_id) + "/fetch/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("status"), True)

    @mock.patch("feedparser.parse")
    def test_fetch_feed_with_bad_request_from_feed(self, mock_feedparser):
        """
        Test for fetch feed manually by user.
        Feed will return invalid data
        """
        assert mock_feedparser is feedparser.parse

        module_dir = os.path.dirname(__file__)
        feedparser_invalid_rss = os.path.join(module_dir, "data", "invalid_rss.json")

        with open(feedparser_invalid_rss, "rb") as f:
            mock_feedparser.return_value = json.loads(f.read())

        user = self.create_user()
        token = self.create_token(user)
        feed = self.create_feed(user)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(self.url + str(feed.pk) + "/fetch/")
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.json().get("status"), False)
        self.assertEqual(
            response.json().get("message"),
            "nodename nor servname provided, or not known",
        )

        feed.refresh_from_db()
        self.assertEqual(feed.attempt, 1)


class FeedItemTests(TestCase):
    """
    Feed Item API Test Case
    """

    url = "/api/feed-item/"

    def test_list_view(self):
        """
        Test API request for getting all feed items
        """
        user = self.create_user()
        token = self.create_token(user)
        feed = self.create_feed(user)
        feed_item = self.create_feed_item(feed, user)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("count"), 1)

    def test_feed_item_favorite(self):
        """
        Test for mark feed item like favorite
        """
        user = self.create_user()
        token = self.create_token(user)
        feed = self.create_feed(user)
        feed_item = self.create_feed_item(feed, user)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(self.url + str(feed_item.pk) + "/favorite/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("is_favorite"), True)

        self.assertEqual(user.favorite_items.filter(pk=feed_item.pk).exists(), True)

        response = self.client.get(self.url + str(feed_item.pk) + "/favorite/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("is_favorite"), False)

        self.assertEqual(user.favorite_items.filter(pk=feed_item.pk).exists(), False)

    def test_feed_item_read(self):
        """
        Test for mark feed like read
        """
        user = self.create_user()
        token = self.create_token(user)
        feed = self.create_feed(user)
        feed_item = self.create_feed_item(feed, user)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(self.url + str(feed_item.pk) + "/read/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("is_read"), True)

        self.assertEqual(user.read_items.filter(pk=feed_item.pk).exists(), True)
