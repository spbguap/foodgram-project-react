from rest_framework import serializers
from rest_framework.authentication import get_user_model

from recipes.models import Recipe

from .models import CustomUser, Subscribe

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    def get_fields(self):
        fields = super().get_fields()
        if self.context['request'].method == 'POST':
            fields['password'] = serializers.CharField(write_only=True)
        else:
            fields.pop('password', None)
        return fields

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=request.user, subscribing=obj.id
        ).exists()


class SubscribeResipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(UserSerializer):
    email = serializers.EmailField(source='subscribing.email')
    id = serializers.IntegerField(source='subscribing.id')
    username = serializers.CharField(source='subscribing.username')
    first_name = serializers.CharField(source='subscribing.first_name')
    last_name = serializers.CharField(source='subscribing.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        limit = self.context.get('request').query_params.get('recipes_limit')

        if limit:
            # fmt: off
            queryset = Recipe.objects.filter(author=obj.subscribing).order_by(
                '-id'
            )[:int(limit)]
            # fmt: on
        else:
            queryset = Recipe.objects.filter(author=obj.subscribing)
        return SubscribeResipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.subscribing).count()


class SubscribeToUserSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=queryset)
    subscribing = serializers.PrimaryKeyRelatedField(queryset=queryset)
    subscribing_user = UserSerializer(source='subscribing', read_only=True)

    class Meta:
        model = Subscribe
        fields = ('user', 'subscribing', 'subscribing_user')

    def validate(self, data):
        request = self.context.get('request')
        subscribing_id = data['subscribing'].id

        subscribe_is_exists = Subscribe.objects.filter(
            user=request.user, subscribing__id=subscribing_id
        ).exists()

        if request.method == 'POST':
            if request.user.id == subscribing_id:
                raise serializers.ValidationError('Нельзя подписаться насебя')
            if subscribe_is_exists:
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого пользователя'
                )

        return data

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop('user')
        result.pop('subscribing')
        return result


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        user = self.context['request'].user

        if not current_password or not new_password:
            raise serializers.ValidationError(
                'Требуется текущий и новый пароль'
            )

        if not user.check_password(current_password):
            raise serializers.ValidationError('Неверный текущий пароль')

        return data
