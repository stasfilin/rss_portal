from django.conf import settings
from django.db import models

from feed.models import FeedItem


class Comment(models.Model):
    """
    Comment model
    Default ordering by date_added. Newest first
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    feed_item = models.ForeignKey(
        FeedItem, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.feed_item}"

    class Meta:
        ordering = ["-date_added"]
