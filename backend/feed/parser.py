import feedparser
from dateutil import parser
from django.conf import settings
from django.utils import timezone

from feed.exceptions import ParsingError
from feed.models import Feed, FeedItem


def feed_parser(feed: Feed) -> Feed:
    """
    Parsing function for getting and save articles to FeedItem Model
    Checking results from feed and if we can't get articles we will add +1 to attempt
    If attempt >= settings.TOTAL_ATTEMPT we will mark this feed like Attempt
    :param feed: Feed Object
    :return: Feed Object
    """
    feed.last_fetch = timezone.now()
    fetch_data = feedparser.parse(feed.url)
    if fetch_data.get("bozo_exception"):
        feed.attempt += 1
        if feed.attempt >= settings.TOTAL_ATTEMPT:
            feed.terminated = True
        feed.save()
        raise ParsingError("nodename nor servname provided, or not known")
    entries = fetch_data.get("entries")

    items = []
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

        items.append(feed_item)

    feed.user.feed_items.add(*items)
    feed.items.add(*items)
    feed.last_updated = timezone.now()
    feed.save()
    return feed
