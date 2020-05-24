from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from faker import Faker

from feed.models import Feed, FeedItem, url_validation
from utils.testcase import TestCaseModelCommands


class TestFeedModel(TestCase, TestCaseModelCommands):
    """
    Test Case for Feed Model
    """

    faker = Faker()

    def test_create_feed_with_valid_url(self):
        """
        Test Feed for creating new feed with valid url
        """
        user = self.create_user()

        data = {"user": user, "url": "http://www.nu.nl/rss/Algemeen", "title": "NU.NL"}

        feed, _ = Feed.objects.get_or_create(**data)

        self.assertEqual(feed.url, data.get("url"))
        self.assertEqual(feed.user, data.get("user"))

    def test_create_feed_with_invalid_url(self):
        """
        Test Feed for creating new feed with invalid url
        """
        user = self.create_user()

        data = {"user": user, "url": "http://www.google.com", "title": "NU.NL"}

        feed = Feed(**data).save()

        self.assertEqual(feed, None)

    def test_url_validation(self):
        """
        Test url validation function
        """
        URLS = (
            ("http://www.nu.nl/rss/Algemeen", True),
            ("https://feeds.feedburner.com/tweakers/mixed", True),
            ("http://www.google.com", False),
        )

        for url in URLS:
            if url[1]:
                self.assertEqual(url_validation(url[0]), None)
            else:
                with self.assertRaises(ValidationError) as e:

                    url_validation(url[0])

                self.assertEqual(e.exception.message, "%(value)s is invalid rss url")


class TestFeedItemModel(TestCase, TestCaseModelCommands):
    """
    Test Case for Feed Item Model
    """

    faker = Faker()

    def test_create_feed_with_valid_data(self):
        """
        Test Feed Item for creating article with valid data

        """
        user = self.create_user()
        feed = self.create_feed(user)

        feed_item, status = FeedItem.objects.get_or_create(
            title=self.faker.sentence(),
            summary=self.faker.text(),
            link=self.faker.url(),
            published=timezone.now(),
        )

        feed_item.feed.add(feed)
        feed_item.user.add(user)
        feed_item.save()

        feed_item.refresh_from_db()

        self.assertEqual(status, True)
        self.assertEqual(user.feed_items.filter(pk=feed_item.pk).exists(), True)
        self.assertEqual(feed.items.filter(pk=feed_item.pk).exists(), True)
