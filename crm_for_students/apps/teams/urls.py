# Django modules
from django.urls import path, include

# DRF modules
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView


from apps.teams.auth_views import (
    CurrentUserView,
    CustomTokenPairView,
    LogoutView,
    RegisterView,
)
from apps.teams.views import TeamViewSet, TeamMembershipViewSet

router: DefaultRouter = DefaultRouter()
router.register(prefix="teams", viewset=TeamViewSet, basename="team")
router.register(
    prefix="membership", viewset=TeamMembershipViewSet, basename="membership"
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", CustomTokenPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", CurrentUserView.as_view(), name="current_user"),
    path("", include(router.urls)),
]
