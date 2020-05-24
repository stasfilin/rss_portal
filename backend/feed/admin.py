from django.contrib import admin

from feed.models import Feed, FeedItem


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    """
    Add Feed Model to Admintool
    """

    list_display = (
        "title",
        "url",
        "create_date",
        "last_fetch",
        "last_updated",
        "attempt",
        "terminated",
    )

    list_filter = (
        "last_fetch",
        "last_updated",
        "attempt",
        "terminated",
    )


@admin.register(FeedItem)
class FeedItemAdmin(admin.ModelAdmin):
    """
    Add Feed Item Model to Admintool
    """

    list_display = (
        "title",
        "link",
        "published",
        "author",
    )

    list_filter = ("author",)
