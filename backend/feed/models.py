import feedparser
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils import timezone


def url_validation(value):
    parsed_feed = feedparser.parse(value)
    if parsed_feed.get("bozo_exception"):
        raise ValidationError(
            "%(value)s is invalid rss url", params={"value": value},
        )


class Feed(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feeds"
    )
    url = models.URLField(max_length=100, blank=False, validators=[url_validation])
    title = models.CharField(max_length=256, blank=True)

    create_date = models.DateTimeField(auto_now_add=True)
    last_fetch = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    attempt = models.PositiveIntegerField(default=0)
    terminated = models.BooleanField(default=False)


class FeedItem(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="items")

    title = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    link = models.URLField(blank=True)
    published = models.DateTimeField()
    author = models.CharField(max_length=50, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feed_items"
    )
    is_favorite = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
