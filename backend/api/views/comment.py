from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.serializers.comment import CommentSerializer
from comment.models import Comment


class CommentView(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):

    queryset = Comment.objects.none()
    serializer_class = CommentSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.comments.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
