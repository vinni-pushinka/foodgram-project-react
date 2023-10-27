from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPaginator
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeSerializer,
                             ShoppingCartSerializer, TagSerializer)
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


def index(request):
    return HttpResponse('index')


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    search_fields = ('^name', )
    filter_backends = (IngredientFilter,)
    permission_classes = (AllowAny,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'recipe_ingredients__ingredient', 'tags'
        ).all()
        return recipes

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'user': user.id,
            'recipe': recipe.id,
        }
        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        get_object_or_404(
            Favorite,
            user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'user': user.id,
            'recipe': recipe.id,
        }
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        get_object_or_404(
            ShoppingCart,
            user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=request.user)
        recipes = shopping_cart.values_list('recipe', flat=True)
        shopping_list = RecipeIngredient.objects.filter(
            recipe__in=recipes).values(
            'ingredient'
        ).annotate(
            total_amount=Sum('amount')
        )

        shopping_list_content = 'Список покупок:\n'
        for item in shopping_list:
            ingredient = Ingredient.objects.get(pk=item['ingredient'])
            amount = item['total_amount']
            shopping_list_content += (
                f'{ingredient.name}, {amount} {ingredient.measurement_unit}\n'
            )

        response = HttpResponse(
            shopping_list_content,
            content_type='text/plain')
        response[
            'Content-Disposition'] = 'attachment; filename="shopping-list.txt"'
        return response
