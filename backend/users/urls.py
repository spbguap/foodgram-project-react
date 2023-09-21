from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (  # SubscribeToUserView,
    ChangePasswordView,
    CurrentUserView,
    CustomUserViewSet,
    SubscribeListViewSet,
)

router = DefaultRouter()

router.register(
    'users/subscriptions', SubscribeListViewSet, basename='subscribe'
)

router.register('users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    # path(
    #     'users/<int:pk>/subscribe/',
    #     SubscribeToUserView.as_view(),
    #     name='user-subscribe',
    # ),
    path(
        'users/set_password/',
        ChangePasswordView.as_view(),
        name='change-password',
    ),
    path('', include(router.urls)),
    path('', include("djoser.urls")),
    path('auth/', include("djoser.urls.authtoken")),
]
