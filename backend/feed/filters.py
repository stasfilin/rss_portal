from django_filters import rest_framework as filters


class FeedItemFilterSet(filters.FilterSet):
    """
    Custom filter for Feed Item API.
    Filtering Articles by favorite, read and unread
    """

    filter = filters.CharFilter(method="get_filter", field_name="custom_filter")

    def get_filter(
        self, queryset, field_name, value,
    ):
        if value:
            if value == "favorite":
                return self.request.user.favorite_items.all()
            elif value == "read":
                return self.request.user.read_items.all()
            elif value == "unread":
                return self.request.user.feed_items.all().exclude(
                    is_read__pk=self.request.user.pk
                )
        return queryset
