from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Dev tool urls
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    ### Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    ### Redoc
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),

    # Actual urls
    path("api/", include("listings.urls")),
    path("api/", include("bookings.urls")),
    path("api/auth/", include("accounts.urls")), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
