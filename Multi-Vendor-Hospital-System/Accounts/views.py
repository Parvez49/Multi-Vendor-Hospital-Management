from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
import datetime

from .models import User, Notification
from .permissions import authenticateUser, IsLoggedIn, IsSuperUser
from .serializers import (
    NotificationSerializer,
    NotificationDetailSerializer,
    PublicUserListSerializer,
)
from .tasks import send_verification_email


from .serializers import UserLoginSerializer  # UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken


class NotificationDelete(DestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            notification = Notification.objects.get(uuid=kwargs["notification_uuid"])
            if request.user.email != notification.recipient.email:
                return Response(
                    {"message": "you are not allowed"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            notification.delete()
            return Response(
                {"message": "Notification deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Notification.DoesNotExist:
            return Response(
                {"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND
            )


class NotificationDetail(ListAPIView):
    serializer_class = NotificationDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        notification_uuid = self.kwargs["notification_uuid"]
        obj = Notification.objects.filter(uuid=notification_uuid).first()
        obj.is_read = True
        obj.save()
        return [obj]


class NotificationList(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)

        email = self.request.user.email
        return Notification.objects.filter(recipient__email=email)


class PublicResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        new_password = request.data.get("new_password")
        confirm_new_password = request.data.get("confirm_new_password")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except ExpiredSignatureError:
            return Response("Token has expired.", status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response("Invalid token.", status=status.HTTP_405_METHOD_NOT_ALLOWED)

        user = User.objects.get(email=payload["email"])

        if new_password == confirm_new_password:
            user.set_password(new_password)
            user.save()
            return Response("Password has been reset successfully.")
        else:
            return Response(
                "New passwords do not match.", status=status.HTTP_400_BAD_REQUEST
            )


from .tasks import send_password_reset_email


class PublicRequestPasswordReset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("ps")
        user = User.objects.filter(email=request.data["email"]).first()
        if not user:
            raise NotFound("User with this email does not exist.")
        else:
            send_password_reset_email.delay(request.data["email"])

            response_data = {
                "message": "Check your email to reset your password.",
            }

            return Response(response_data, status=status.HTTP_201_CREATED)


class PublicUserLogout(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie("logintoken")
        response.data = {"you are logged out"}
        response.status_code = status.HTTP_200_OK
        return response


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(
                {"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.filter()


# class UserInfoView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)


"""
class PublicUserLogin(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.filter(email=email).first()

        if not user:
            raise AuthenticationFailed("User not found!")
        if user.is_active == False:
            raise AuthenticationFailed("Check your email to activate your account...")
        if not check_password(password, user.password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            # 'uuid': user.uuid,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()
        response.set_cookie(key="logintoken", value=token, httponly=True)
        response.data = {"You are logged in"}

        return response
"""


class PublicUserRetrieveUpdateDestroy(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PublicUserListSerializer

    def get_queryset(self):
        email = self.request.user.email
        return User.objects.filter(email=email)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


from rest_framework.permissions import IsAdminUser


class PrivateUserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserListSerializer
    # permission_classes = [IsSuperUser]
    permission_classes = [IsAdminUser]


class PublicVerifyAccount(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except ExpiredSignatureError:
            return Response("Token has expired.", status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response("Invalid token.", status=status.HTTP_405_METHOD_NOT_ALLOWED)

        user = User.objects.get(email=payload["email"])
        user.is_active = True
        user.save()
        return Response(
            {"Success": "Activated your account"}, status=status.HTTP_200_OK
        )


class PublicUserCreate(CreateAPIView):
    serializer_class = PublicUserListSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = request.data["email"]

            # Send the verification email asynchronously using Celery
            send_verification_email.delay(email)

            response_data = {
                "message": "Account created. Check your email to activate your account.",
            }
            # serializer.save()
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
