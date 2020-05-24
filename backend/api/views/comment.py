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
    """
    Comment View for adding, update and remove comment
    """

    queryset = Comment.objects.none()
    serializer_class = CommentSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Change queryset to user comments
        :return: User comments queryset
        """
        return self.request.user.comments.all()

    def perform_create(self, serializer):
        """
        Add user when he create new comment
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Add user when he update comment
        """
        serializer.save(user=self.request.user)
