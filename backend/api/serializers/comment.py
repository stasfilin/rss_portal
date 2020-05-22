from rest_framework import serializers

from comment.models import Comment
from feed.models import FeedItem


class CommentSerializer(serializers.ModelSerializer):
    feed_item_id = serializers.ModelField(
        FeedItem._meta.get_field("id"),
        required=True,
        help_text="Feed Item ID",
        write_only=True,
    )
    date_added = serializers.DateTimeField(read_only=True, format="%B %e,%l:%M %p")

    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "date_added",
            "feed_item_id",
        )
