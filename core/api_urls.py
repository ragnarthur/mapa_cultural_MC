# core/api_urls.py
from rest_framework.routers import DefaultRouter
from .views import AgentViewSet, SpaceViewSet, EventViewSet

router = DefaultRouter()
router.register(r'agents', AgentViewSet)
router.register(r'spaces', SpaceViewSet)
router.register(r'events', EventViewSet)

urlpatterns = router.urls
