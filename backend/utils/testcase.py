from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
from faker import Faker
from rest_framework.test import APITestCase
from rest_framework_jwt.utils import jwt_create_payload, jwt_encode_payload

from feed.models import Feed, FeedItem


class TestCaseModelCommands(object):
    def create_user(self) -> User:
        """
        Function for creating user
        :return: User Object
        """
        user_password = get_random_string()
        user_data = {
            "username": self.faker.first_name(),
            "password": user_password,
            "email": self.faker.email(),
        }
        user = User.objects.create_user(**user_data)

        return user

    def create_token(self, user: User) -> str:
        """
        Function for creating JWT token for user
        :param user: User Object
        :return: token
        """
        payload = jwt_create_payload(user)
        token = jwt_encode_payload(payload)
        return token

    def create_feed(self, user: User) -> Feed:
        """
        Function for creating Feed
        :param user: User Object
        :return: Feed Object
        """
        feed, _ = Feed.objects.get_or_create(
            user=user, url="http://www.nu.nl/rss/Algemeen", title="NU.NL"
        )

        return feed

    def create_feed_item(self, feed: Feed, user: User) -> FeedItem:
        """
        Function for creating fake FeedItem
        :param feed: Feed Object
        :param user: User Object
        :return: FeedItem object
        """
        feed_item, _ = FeedItem.objects.get_or_create(
            title=self.faker.sentence(),
            summary=self.faker.text(),
            link=self.faker.url(),
            published=timezone.now(),
        )

        feed_item.feed.add(feed)
        feed_item.user.add(user)

        return feed_item


class TestCase(APITestCase, TestCaseModelCommands):
    """
    Custom TestCase for checking API
    """

    faker = Faker()
