from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.serializers.feed import FeedSerializer
from feed.models import Feed


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
