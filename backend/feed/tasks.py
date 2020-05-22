from celery.task import periodic_task, task
from celery.schedules import crontab
from feed.models import Feed
from feed.parser import feed_parser


@periodic_task(
    run_every=(crontab(minute="*/10")), name="fetch_feeds", ignore_result=True
)
def fetch_feeds():
    feeds = Feed.objects.filter(terminated=False)
    total = 0
    for feed in feeds:
        try:
            res = feed_parser(feed)
            total += 1
        except Exception as e:
            pass
    return total
