from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.validators import (
    UniqueTogetherValidator, ValidationError)

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import CustomUser, Follow
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipe_ingredients'
    )
    image = Base64ImageField(required=False, allow_null=True, max_length=None)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request:
            return Favorite.objects.filter(
                user=request.user.id,
                recipe=obj.id).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request:
            return ShoppingCart.objects.filter(
                user=request.user.id,
                recipe=obj.id).exists()
        return False

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'author', 'image',
            'ingredients', 'tags', 'text', 'cooking_time',
            'is_favorited', 'is_in_shopping_cart',
        )


class MiniRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')


class RecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField(required=False, allow_null=True,  max_length=None)

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'name', 'cooking_time',
            'text', 'tags', 'ingredients', 'image',
            )

    def add_ingredients(self, ingredients_data, instance):
        for ingredient_data in ingredients_data:
            amount = ingredient_data['amount']
            ingredient = ingredient_data['id']
            RecipeIngredient.objects.get_or_create(
                recipe=instance,
                ingredient=ingredient,
                amount=amount)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        instance = Recipe.objects.create(author=author, **validated_data)
        self.add_ingredients(ingredients_data, instance)
        instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        self.add_ingredients(ingredients_data, instance)
        instance.tags.set(tags)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance).data


class FollowListSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения подписок пользователя."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'recipes',
                  'recipes_count',)

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = Recipe.objects.filter(author=obj)
        if request:
            recipes_limit = request.GET.get('recipes_limit')
            if recipes_limit:
                recipes = recipes[: int(recipes_limit)]
        serializer = MiniRecipeSerializer(
            recipes,
            many=True,
            read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки на пользователя."""

    class Meta:
        model = Follow
        fields = ('user', 'author',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
                message='Вы уже подписаны на этого автора!',
            )
        ]

        def validate(self, data):
            if self.context['request'].user == data['author']:
                raise ValidationError(
                    code=status.HTTP_400_BAD_REQUEST,
                    detail='Нельзя подписаться на самого себя!')
            return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return FollowListSerializer(
            instance.author,
            context={'request': request}).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe',)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe',)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
