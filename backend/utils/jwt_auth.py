from api.serializers.user import UserBaseSerializer


def jwt_create_response_payload(token, user=None, request=None, issued_at=None):
    return {
        "token": token,
        "user": UserBaseSerializer(user).data,
    }
