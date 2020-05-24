import json
import os
from unittest import mock

import feedparser
from django.conf import settings
from django.test import TestCase
from faker import Faker

from feed.exceptions import ParsingError
from feed.parser import feed_parser
from utils.testcase import TestCaseModelCommands


class ParserTests(TestCase, TestCaseModelCommands):
    """
    Parser Test Case
    """

    faker = Faker()

    @mock.patch("feedparser.parse")
    def test_parser_with_invalid_data(self, mock_feedparser):
        """
        Test for parser with invalid data.
        feedparser mocked for invalid data
        """
        assert mock_feedparser is feedparser.parse

        module_dir = os.path.dirname(__file__)
        feedparser_invalid_rss = os.path.join(module_dir, "data", "invalid_rss.json")

        with open(feedparser_invalid_rss, "rb") as f:
            mock_feedparser.return_value = json.loads(f.read())

        user = self.create_user()
        feed = self.create_feed(user)

        with self.assertRaises(ParsingError) as e:
            feed_parser(feed)
        self.assertEqual(
            e.exception.message, "nodename nor servname provided, or not known"
        )

        feed.refresh_from_db()
        self.assertEqual(feed.attempt, 1)

    @mock.patch("feedparser.parse")
    def test_terminate_feed(self, mock_feedparser):
        """
        Test for mark feed like terminate
        """
        assert mock_feedparser is feedparser.parse

        module_dir = os.path.dirname(__file__)
        feedparser_invalid_rss = os.path.join(module_dir, "data", "invalid_rss.json")

        with open(feedparser_invalid_rss, "rb") as f:
            mock_feedparser.return_value = json.loads(f.read())

        user = self.create_user()
        feed = self.create_feed(user)

        self.assertEqual(feed.terminated, False)

        for step in range(1, settings.TOTAL_ATTEMPT + 1):
            with self.assertRaises(ParsingError) as e:
                feed_parser(feed)
            self.assertEqual(
                e.exception.message, "nodename nor servname provided, or not known"
            )
            feed.refresh_from_db()
            self.assertEqual(feed.attempt, step)

        self.assertEqual(feed.terminated, True)
