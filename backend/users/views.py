from django.contrib.auth.hashers import check_password
from djoser.views import UserViewSet
from rest_framework import (
    filters,
    generics,
    mixins,
    permissions,
    status,
    viewsets,
)
from rest_framework.authentication import get_user_model
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from users.models import Subscribe

from .serializers import SubscribeSerializer, UserSerializer

User = get_user_model()


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination


class SubscribeListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SubscribeSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('subscribing__username', 'subscriber__username')
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.request.user.subscriber.all()


class SubscribeToUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user_to_subscribe = self.get_user(pk)
        if user_to_subscribe is None:
            return Response(
                {"errors": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        current_user = self.request.user
        if current_user == user_to_subscribe:
            return Response(
                {"errors": "Нельзя подписаться на самого себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription, created = Subscribe.objects.get_or_create(
            user=current_user, subscribing=user_to_subscribe
        )
        if not created:
            return Response(
                {"errors": "Вы уже подписаны на этого пользователя."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Подписка успешна."},
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, pk):
        user_to_unsubscribe = self.get_user(pk)
        if user_to_unsubscribe is None:
            return Response(
                {"errors": "Пользователь не найден."},
                status=status.HTTP_404_NOT_FOUND,
            )

        current_user = self.request.user
        try:
            subscription = Subscribe.objects.get(
                user=current_user, subscribing=user_to_unsubscribe
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Subscribe.DoesNotExist:
            return Response(
                {"errors": "Вы не подписаны на этого пользователя."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None


class ChangePasswordView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        user = request.user

        if not current_password or not new_password:
            return Response(
                {"errors": "Требуется текущий и новый пароль"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not check_password(current_password, user.password):
            return Response(
                {"errors": "Неверный текущий пароль."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"detail": "Пароль успешно изменен."},
            status=status.HTTP_200_OK,
        )
