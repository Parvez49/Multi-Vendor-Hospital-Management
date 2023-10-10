from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(
        "/notifications/<uuid:notification_uuid>/delete",
        views.NotificationDelete.as_view(),
        name="notification-Delete",
    ),
    path(
        "/notifications/<uuid:notification_uuid>",
        views.NotificationDetail.as_view(),
        name="notification-Detail",
    ),
    path(
        "/notifications",
        views.NotificationList.as_view(),
        name="notification-list",
    ),
    path(
        "/password/reset/<str:token>",
        views.PublicResetPassword.as_view(),
        name="user-reset-password",
    ),
    path(
        "/password/reset",
        views.PublicRequestPasswordReset.as_view(),
        name="user-request-password",
    ),
    # path("/logout", views.PublicUserLogout.as_view(), name="user-logout"),
    # path("/logout", views.UserLogoutView.as_view(), name="token-logout"),
    path("/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("/login", views.UserLoginView.as_view(), name="user-login"),
    path(
        "/me",
        views.PublicUserRetrieveUpdateDestroy.as_view(),
        name="user-detail",
    ),
    path("/list", views.PrivateUserList.as_view(), name="user-list"),
    path(
        "/verify/<str:token>",
        views.PublicVerifyAccount.as_view(),
        name="user-verify-account",
    ),
    path("/register", views.PublicUserCreate.as_view(), name="user-register"),
    # path("/api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("/api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
