from dateutil import parser
import feedparser
from django.utils import timezone

from feed.models import Feed, FeedItem


def feed_parser():
    for feed in Feed.objects.filter(terminated=False):
        feed.last_fetch = timezone.now()
        fetch_data = feedparser.parse(feed.url)
        if fetch_data.get("bozo_exception"):
            feed.attempt += 1
            feed.save()
            continue
        entries = fetch_data.get("entries")

        for article in entries:
            defaults = {
                "feed": feed,
                "title": article.get("title"),
                "summary": article.get("summary"),
                "link": article.get("link"),
                "published": parser.parse(article.get("published")),
                "author": article.get("author"),
                "user": feed.user,
            }
            feed_item, _ = FeedItem.objects.get_or_create(
                link=article.get("link"), defaults=defaults
            )

        feed.save()

        feed.last_updated = timezone.now()
        feed.save()
