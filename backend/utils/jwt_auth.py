from api.serializers.user import UserBaseSerializer


def jwt_create_response_payload(token, user=None, request=None, issued_at=None) -> dict:
    """
    Function for adding User Object to AUTH function
    :param token: token
    :param user: User Object
    :param request: Django Request
    :param issued_at: Datetime
    :return: dict
    """
    return {
        "token": token,
        "user": UserBaseSerializer(user).data,
    }
