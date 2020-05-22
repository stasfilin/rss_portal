from dateutil import parser
import feedparser
from django.utils import timezone
from django.conf import settings

from feed.models import Feed, FeedItem


def feed_parser(feed: Feed):
    feed.last_fetch = timezone.now()
    fetch_data = feedparser.parse(feed.url)
    if fetch_data.get("bozo_exception"):
        feed.attempt += 1
        if feed.attempt >= settings.TOTAL_ATTEMPT:
            feed.terminated = True
        feed.save()
        raise Exception("nodename nor servname provided, or not known")
    entries = fetch_data.get("entries")

    for article in entries:
        defaults = {
            "title": article.get("title"),
            "summary": article.get("summary"),
            "link": article.get("link"),
            "published": parser.parse(article.get("published")),
            "author": article.get("author"),
        }
        feed_item, _ = FeedItem.objects.get_or_create(
            link=article.get("link"), defaults=defaults
        )
        feed_item.user.add(feed.user)
        feed_item.feed.add(feed)
        feed_item.save()

    feed.save()

    feed.last_updated = timezone.now()
    feed.save()
    return feed
