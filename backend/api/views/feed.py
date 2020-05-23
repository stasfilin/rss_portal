from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.serializers.feed import FeedSerializer, FeedItemSerializer
from feed.filters import FeedItemFilterSet
from feed.models import Feed, FeedItem
from feed.parser import feed_parser


class FeedView(ModelViewSet):
    queryset = Feed.objects.none()
    serializer_class = FeedSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.feeds.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"])
    def fetch(self, request, pk=None):
        feed = self.get_object()
        try:
            feed_parser(feed)
            return Response({"status": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class FeedItemView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = FeedItem.objects.none()
    serializer_class = FeedItemSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = FeedItemFilterSet

    def get_queryset(self):
        return self.request.user.feed_items.all()

    def get_serializer_context(self):
        return {
            "request": self.request,
        }

    @action(detail=True, methods=["get"])
    def favorite(self, request, pk=None):
        feed_item = self.get_object()
        user = request.user
        if feed_item.is_favorite.filter(pk=user.pk):
            feed_item.is_favorite.remove(user)
        else:
            feed_item.is_favorite.add(user)
        feed_item.save()

        return Response({"is_favorite": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def read(self, request, pk=None):
        feed_item = self.get_object()
        user = request.user
        feed_item.is_read.add(user)
        feed_item.save()

        return Response({"is_read": True}, status=status.HTTP_200_OK)
