from django.urls import path
from .views import GoogleAuthView, Logout, GrantLeaseManagementView, JWTTokenRefreshView, Protected, Me, OnboardingView

urlpatterns = [
    path("google/", GoogleAuthView.as_view(), name="auth_google"),
    path(
        "capabilities/leasing/manage/",
        GrantLeaseManagementView.as_view(),
        name="auth_grant_manage_leases",
    ),
    path("token/refresh/", JWTTokenRefreshView.as_view(), name="token_refresh"),
    path("protected/", Protected.as_view(), name="protected"),
    path("me/", Me.as_view(), name="me"),
    path("onboarding/", OnboardingView.as_view(), name="onboarding"),
    path("logout/", Logout.as_view(), name="logout"),
]
