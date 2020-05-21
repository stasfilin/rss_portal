from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from api.views import user as user_view
from api.views import feed as feed_view
from api.views import comment as comment_view

urlpatterns = [
    path("signin/", obtain_jwt_token, name="signin_token_obtain"),
    path("token/refresh/", refresh_jwt_token, name="token_refresh"),
    path("token/verify/", verify_jwt_token, name="token_verify"),
]

router = routers.SimpleRouter()

router.register(r"signup", user_view.SignUpView)
router.register(r"feed", feed_view.FeedView)
router.register(r"feed-item", feed_view.FeedItemView)
router.register(r"comment", comment_view.CommentView)

urlpatterns.extend(router.urls)
