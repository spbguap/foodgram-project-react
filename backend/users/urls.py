from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChangePasswordView  # SubscribeListViewSet,;
from .views import CustomUserViewSet  # UserDetailView,
from .views import SubscribeListViewSet  # UserDetailView,
from .views import CurrentUserView, SubscribeToUserView

router = DefaultRouter()

router.register(
    r'users/subscriptions', SubscribeListViewSet, basename='subscribe'
)

router.register(r'users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path(
        'users/<int:pk>/subscribe/',
        SubscribeToUserView.as_view(),
        name='user-subscribe',
    ),
    path(
        'users/set_password/',
        ChangePasswordView.as_view(),
        name='change-password',
    ),
    path('', include(router.urls)),
    path('', include("djoser.urls")),
    path('auth/', include("djoser.urls.authtoken")),
]
