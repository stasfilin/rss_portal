from rest_framework import serializers

from feed.models import Feed, FeedItem


class FeedSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(read_only=True)
    last_fetch = serializers.DateTimeField(read_only=True)
    last_updated = serializers.DateTimeField(read_only=True)
    attempt = serializers.IntegerField(read_only=True)
    terminated = serializers.BooleanField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Feed
        fields = (
            "id",
            "url",
            "title",
            "create_date",
            "last_fetch",
            "last_updated",
            "attempt",
            "terminated",
        )


class FeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedItem
        fields = (
            "id",
            "title",
            "summary",
            "link",
            "published",
            "author",
            "is_favorite",
            "is_read",
        )
