from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.serializers.user import SignUpSerializer


class SignUpView(mixins.CreateModelMixin, GenericViewSet):
    """
    Sign Up View.
    Permission - AllowAny, all people can create new user
    """

    queryset = User.objects.none()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)
    authentication_classes = [JSONWebTokenAuthentication]
