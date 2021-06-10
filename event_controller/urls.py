from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import EventMainView, EventAttenderView

router = DefaultRouter()
router.register("event", EventMainView)
router.register("event-attender", EventAttenderView)

urlpatterns = [
	path("", include(router.urls))
]