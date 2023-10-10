from rest_framework.permissions import BasePermission
from rest_framework.exceptions import (
    PermissionDenied,
    AuthenticationFailed,
    ValidationError,
)
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError

from Accounts.models import User


def authenticateUser(token):
    # helper function for checking whether user log in or not

    if not token:
        raise AuthenticationFailed({"error": "Log in first!"})
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except ExpiredSignatureError:
        raise AuthenticationFailed({"error": "You session has expired!"})
    except DecodeError:
        raise AuthenticationFailed({"error": "Log in failed!"})
    return payload


class IsLoggedIn(BasePermission):
    def has_permission(self, request, view):
        print("permission")
        token = request.COOKIES.get("logintoken")
        payload = authenticateUser(token)
        if payload:
            return True
        else:
            raise PermissionDenied("Log in First!!!")


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        token = request.COOKIES.get("logintoken")
        payload = authenticateUser(token)
        email = payload["email"]
        user = User.objects.filter(email=email).first()

        if user.is_superuser == True:
            return True
        else:
            # return False
            raise PermissionDenied(
                "You are not superuser. Only Super User has permission!!!"
            )
