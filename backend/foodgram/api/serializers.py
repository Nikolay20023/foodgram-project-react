from rest_framework import serializers
from django.contrib.auth import get_user_model
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    ShoppingCart,
    Favourite,
    RecipeIngredient
)
from users.serializers import CustomUserSerializator
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import F
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from core.services import recipe_ingredients_set
from collections import OrderedDict
from django.core.exceptions import ValidationError
from core.validators import tags_exist_validators, ingredients_validator


User = get_user_model()


class IngredientSerialier(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__',


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.IntegerField(write_only=True, min_value=1)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'amount', 'id')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__',

    def validate(self, data: OrderedDict) -> OrderedDict:
        for attr, value in data.items():
            data[attr] = value.sttrip(' #').upper()

        return data


class ShoppingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favourite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное'
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializator(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'tags',
            'text',
            'ingredients',
            'cooking_time',
            'image',
            'is_favorited',
            'is_in_shopping_cart'
        )
        read_only_fields = (
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_ingredients(self, recipe: Recipe):
        ingredients = recipe.ingredients.values(
            'id', 'name', 'units', amount=F('ingredient_recipes__amount')
        )
        return ingredients

    def get_is_favorited(self, recipe: Recipe):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe: Recipe):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return user.user_cart.filter(recipe=recipe).exists()

    def validate(self, data):
        tags_ids = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')

        if not tags_ids or not ingredients:
            raise ValidationError(
                f'Ошибка в {tags_ids}, {ingredients}'
            )
        tags_exist_validators(tags_ids, Tag)
        ingredients = ingredients_validator(ingredients, Ingredient)

        data.update(
            {
                'tags': tags_ids,
                'ingredients': ingredients,
                'author': self.context.get('request').user
            }
        )
        return data

    def create(self, validated_data: dict):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe_ingredients_set(recipe, ingredients)

        return recipe

    @atomic
    def update(self, recipe: dict, validate_data: Recipe):

        tags = validate_data.pop("tags")
        ingredients = validate_data.pop('ingredients')
        for key, value in validate_data.items():
            if hasattr(recipe, key):
                setattr(recipe, key, value)

        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)

        if ingredients:
            recipe.ingredients.clear()
            recipe_ingredients_set(recipe, ingredients)

        recipe.save()
        return recipe
