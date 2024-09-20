from django.urls import path
from django.conf.urls import include

from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet
from api.views import department, location, device, log, invitation

router = DefaultRouter()
router.register("auth/users", UserViewSet)
router.register("department", department.DepartmentViewSet)
router.register("location", location.LocationViewSet)
router.register("device", device.DeviceViewSet)
router.register("log", log.LogViewSet)
router.register("invitation", invitation.InvitationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
