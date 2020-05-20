from django.contrib import admin

from feed.models import Feed, FeedItem


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    pass


@admin.register(FeedItem)
class FeedItemAdmin(admin.ModelAdmin):
    pass
