from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import ListingViewSet, ListingImageViewSet

router = DefaultRouter()
router.register(r"listings", ListingViewSet, basename="listing")

listings_router = routers.NestedSimpleRouter(router, r"listings", lookup="listing")
listings_router.register(r"images", ListingImageViewSet, basename="listing-images")

urlpatterns = [*router.urls, *listings_router.urls]