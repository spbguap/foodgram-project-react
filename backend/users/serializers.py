from rest_framework import serializers

from recipes.models import Recipe

from .models import CustomUser, Subscribe


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
            queryset = Recipe.objects.filter(author=obj.subscribing).order_by(
                '-id'
            )[: int(limit)]
        else:
            queryset = Recipe.objects.filter(author=obj.subscribing)
        return SubscribeResipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.subscribing).count()
