from django.contrib import admin

from .models import Favorites, Ingredient, Recipe, ShoppingCart, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('^name',)
    list_filter = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite')
    inlines = (RecipeIngredientInline,)
    list_filter = ('name', 'tags', 'author')

    def favorite(self, obj):
        counter = Favorites.objects.filter(recipe=obj).count()
        return counter


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(ShoppingCart)
admin.site.register(Favorites)
