from django.urls import path

from .views import GoogleAuthView, GrantLeaseManagementView, JWTTokenRefreshView

urlpatterns = [
    path("google/", GoogleAuthView.as_view(), name="auth_google"),
    path(
        "capabilities/leasing/manage/",
        GrantLeaseManagementView.as_view(),
        name="auth_grant_manage_leases",
    ),
    path("token/refresh/", JWTTokenRefreshView.as_view(), name="token_refresh"),
]
