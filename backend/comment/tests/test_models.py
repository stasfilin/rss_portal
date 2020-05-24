from django.test import TestCase
from faker import Faker

from comment.models import Comment
from utils.testcase import TestCaseModelCommands


class CommentModelTests(TestCase, TestCaseModelCommands):
    """
    Comment Test case
    """

    faker = Faker()

    def test_comment_with_valid_data(self):
        """
        Test creating Comment with valid data
        :return:
        """
        user = self.create_user()
        feed = self.create_feed(user)
        feed_item = self.create_feed_item(feed, user)

        data = {"user": user, "feed_item": feed_item, "content": "Test"}

        comment, status = Comment.objects.get_or_create(**data)

        self.assertEqual(status, True)
        self.assertEqual(user.comments.filter(pk=comment.pk).exists(), True)
        self.assertEqual(feed_item.comments.filter(pk=comment.pk).exists(), True)
