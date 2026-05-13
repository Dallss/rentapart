from django.urls import path

from .views import GoogleAuthView, JWTTokenRefreshView, SetRoleView

urlpatterns = [
    path("google/", GoogleAuthView.as_view(), name="auth_google"),
    path("role/", SetRoleView.as_view(), name="auth_set_role"),
    path("token/refresh/", JWTTokenRefreshView.as_view(), name="token_refresh"),
]
