from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.fields import MinValueValidator

from .const import MEASUREMENT_LENGTH, NAME_LENGTH, SLUG_LENGTH

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=NAME_LENGTH, unique=True)
    color = ColorField(default='#FF0000')
    slug = models.SlugField(max_length=SLUG_LENGTH, unique=True)

    class Meta:
        verbose_name = 'Таг'
        verbose_name_plural = 'Таги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_LENGTH)
    image = models.ImageField(
        upload_to='recipes/images/', null=True, default=None
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
    )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveIntegerField(
        validators=(MinValueValidator(1),)
    )

    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецпты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)
    measurement_unit = models.CharField(max_length=MEASUREMENT_LENGTH)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique_ingtidient'
            )
        ]

    def __str__(self):
        return f"{self.name} {self.measurement_unit}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name='recipe_ingredients', on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'recipe',
                    'ingredient',
                ),
                name='recipe_ingredient_unique',
            )
        ]

    def __str__(self):
        return (
            f"{self.ingredient.name} "
            f"{self.amount} {self.ingredient.measurement_unit}"
        )


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_subscriber',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f"{self.recipe} в избранном у {self.user} "


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='customers',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return (
            f'Рецепт {self.recipe.name} '
            f'из списка покупок {self.user.username}'
        )
