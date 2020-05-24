import feedparser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def url_validation(value) -> None:
    """
    URL validation function.
    Checking if this is RSS url
    :param value: url
    :return: None
    """
    parsed_feed = feedparser.parse(value)
    if parsed_feed.get("bozo_exception"):
        raise ValidationError(
            "%(value)s is invalid rss url", params={"value": value},
        )


class Feed(models.Model):
    """
    Feed Model
    Main model, user can add feed with custom title
    """

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

    def __str__(self):
        return f"{self.title}"


class FeedItem(models.Model):
    """
    Feed Item model
    Main model for articles

    Adding some database optimization. Fields: feed, users, is_favorite, is_read = ManyToMany.
    The main reason for this is that few user can add the same Feed URL, so we can store only one Article for few users.

    For is_favorite and is_read in future we can add Article Global Statistic. All users can see how many users add
    mark this article like a favorite
    """

    feed = models.ManyToManyField(Feed, related_name="items")

    title = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    link = models.URLField(blank=True)
    published = models.DateTimeField()
    author = models.CharField(max_length=50, blank=True)

    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="feed_items")
    is_favorite = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="favorite_items"
    )
    is_read = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="read_items"
    )

    class Meta:
        ordering = ["-published"]

    def __str__(self):
        return f"{self.title}"
