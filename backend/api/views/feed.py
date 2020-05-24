import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.serializers.feed import FeedSerializer, FeedItemSerializer
from feed.exceptions import ParsingError
from feed.filters import FeedItemFilterSet
from feed.models import Feed, FeedItem
from feed.parser import feed_parser

logger = logging.getLogger(__name__)


class FeedView(ModelViewSet):
    """
    Feed View
    Users can see only own Feeds
    """

    queryset = Feed.objects.none()
    serializer_class = FeedSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Change queryset to user feeds
        :return: User feeds queryset
        """
        return self.request.user.feeds.all()

    def perform_create(self, serializer):
        """
        Add user when he create new feed
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Add user when he update own feed
        """
        serializer.save(user=self.request.user, attempt=0, terminated=False)

    @action(detail=True, methods=["get"])
    def fetch(self, request, pk=None) -> Response:
        """
        Action for fetch feed manually
        :param request: Django Request
        :param pk: Feed ID
        :return: Response with statuses 200 if valid and 503 if not
        """
        feed = self.get_object()
        try:
            feed_parser(feed)
            return Response({"status": True}, status=status.HTTP_200_OK)
        except ParsingError as e:
            logger.exception(e)
            return Response(
                {"status": False, "message": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    @action(detail=False, methods=["get"])
    def fetch_all(self, request) -> Response:
        """
        Action for fetch feed manually
        :param request: Django Request
        :param pk: Feed ID
        :return: Response with statuses 200 if valid and 503 if not
        """
        feeds = self.get_queryset()
        total = 0
        for feed in feeds:
            try:
                feed_parser(feed)
                total += 1
            except ParsingError as e:
                logger.exception(e)
        return Response(
            {"total": feeds.count(), "finished": total}, status=status.HTTP_200_OK
        )


class FeedItemView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    Feed Item View
    User can see only own Articles
    """

    queryset = FeedItem.objects.none()
    serializer_class = FeedItemSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = FeedItemFilterSet

    def get_queryset(self):
        """
        Change queryset to user feed items
        :return: User feed items queryset
        """
        return self.request.user.feed_items.all()

    def get_serializer_context(self):
        """
        Add request to serializer context
        """
        return {
            "request": self.request,
        }

    @action(detail=True, methods=["get"])
    def favorite(self, request, pk=None):
        """
        Action for mark feed item like favorite or remove this mark
        :param request: Django Request
        :param pk: Feed Item ID
        :return: {"is_favorite": True/False}
        """
        feed_item = self.get_object()
        user = request.user
        if feed_item.is_favorite.filter(pk=user.pk):
            feed_item.is_favorite.remove(user)
            is_favorite = False
        else:
            feed_item.is_favorite.add(user)
            is_favorite = True
        feed_item.save()

        return Response({"is_favorite": is_favorite}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def read(self, request, pk=None):
        """
        Action for mark feed item like read
        :param request: Django Request
        :param pk: Feed Item ID
        :return: {"is_read": True}
        """
        feed_item = self.get_object()
        user = request.user
        feed_item.is_read.add(user)
        feed_item.save()

        return Response({"is_read": True}, status=status.HTTP_200_OK)
