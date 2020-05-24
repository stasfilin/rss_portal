from rest_framework import serializers

from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Serializer
    Read Only Field: date_added
    """

    date_added = serializers.DateTimeField(read_only=True, format="%B %e,%l:%M %p")

    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "date_added",
            "feed_item",
        )
        extra_kwargs = {"feed_item": {"write_only": True}}
