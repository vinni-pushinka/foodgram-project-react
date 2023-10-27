import django_filters
import rest_framework.filters

from recipes.models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):

    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = django_filters.filters.NumberFilter(
        method='fav_filter')
    is_in_shopping_cart = django_filters.filters.NumberFilter(
        method='shopping_cart_filter')

    def fav_filter(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            return queryset.filter(fav_recipe__user=user.id)
        return queryset

    def shopping_cart_filter(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            return queryset.filter(cart_recipe__user=user.id)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart',)


class IngredientFilter(rest_framework.filters.SearchFilter):
    search_param = 'name'
