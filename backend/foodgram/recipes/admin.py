from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag)


class RecipeIngredientInLine(admin.TabularInline):
    """Класс для отображения ингредиентов в рецепте в админке."""
    model = RecipeIngredient
    extra = 1
    min_num = 1


class RecipeTagInLine(admin.TabularInline):
    """Класс для отображения ингредиентов в рецепте в админке."""
    model = RecipeTag
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Класс для отображения тегов в админке."""
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Класс для отображения рецептов в админке."""
    inlines = (RecipeIngredientInLine, RecipeTagInLine,)
    list_display = ('name', 'author', 'get_is_favorited')
    list_filter = ('author', 'name', 'tags')

    def get_is_favorited(self, obj):
        """Метод для определения числа добавлений в избранное."""
        return obj.fav_recipe.count()

    get_is_favorited.short_description = 'Добавили в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Класс для отображения ингредиентов в админке."""
    list_display = ('name', 'measurement_unit', 'id')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Класс для отображения избранного в админке."""
    list_display = ('recipe', 'user', 'id')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Класс для отображения списков покупок в админке."""
    list_display = ('recipe', 'user', 'id')
